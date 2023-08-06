# coding: utf-8

import abc
import asyncio
import itertools
import logging
import warnings
from threading import Lock
from typing import Callable, TYPE_CHECKING, Union

from . import http_service
from .event_code import EventCode
from ._dacs_params import DacsParams
from ._session_cxn_type import SessionCxnType
from .tools import is_closed
from ... import _configure as configure, _log as log
from ..._open_state import OpenState
from ..._tools import DEBUG, cached_property, create_repr

if TYPE_CHECKING:
    from ._session_cxn_factory import SessionConnection
    from .http_service import HTTPService
    from ..._configure import _RDPConfig

SESSION_IS_CLOSED = "Session is closed"


class Session(abc.ABC):
    _id_iterator = itertools.count()
    # Logger for messages outside of particular session instances

    __acquire_session_id_lock = Lock()

    @staticmethod
    def class_logger():
        return log.create_logger("session")

    @property
    def name(self):
        return self._name

    def __init__(
        self,
        app_key,
        on_state: Callable[["Session", OpenState, str], None] = None,
        on_event: Callable[["Session", EventCode, Union[dict, str]], None] = None,
        token=None,
        deployed_platform_username=None,
        dacs_position=None,
        dacs_application_id=None,
        name="default",
    ):
        with self.__acquire_session_id_lock:
            self._session_id = next(self._id_iterator)

        session_type = self.type.name.lower()
        logger_name = f"sessions.{session_type}.{name}.{self.session_id}"

        self.class_logger().debug(
            f'Creating session "{logger_name}" based on '
            f'session.{session_type}.Definition("{session_type}.{name}")'
        )

        if app_key is None:
            raise ValueError("app_key value can't be None")

        self._state = OpenState.Closed

        self._app_key = app_key
        self._on_state: Callable[[Session, OpenState, str], None] = on_state
        self._on_event: Callable[
            [Session, EventCode, Union[dict, str]], None
        ] = on_event
        self._access_token = token
        self._dacs_params = DacsParams()

        if deployed_platform_username:
            self._dacs_params.deployed_platform_username = deployed_platform_username
        if dacs_position:
            self._dacs_params.dacs_position = dacs_position
        if dacs_application_id:
            self._dacs_params.dacs_application_id = dacs_application_id

        self._logger = log.create_logger(logger_name)
        # redirect log method of this object to the log in logger object
        self.log = self._logger.log
        self.warning = self._logger.warning
        self.error = self._logger.error
        self.debug = self._logger.debug
        self.info = self._logger.info

        self._name = name
        self._config: "_RDPConfig" = configure.get_config().copy()

        # override session api config with session's specific api parameters
        specific_api_path = f"sessions.{session_type}.{name}.apis"
        specific_api = self._config.get(specific_api_path)
        if specific_api:
            self._config.set_param("apis", specific_api)

        self._config.on(configure.ConfigEvent.UPDATE, self._on_config_updated)
        # rssl/rwf stream ids always starts with 5
        self._omm_stream_counter = itertools.count(5)

        self._rdp_stream_counter = itertools.count(5)  # can not be 0

    @cached_property
    def _http_service(self) -> "HTTPService":
        return http_service.get_service(self)

    @cached_property
    def _connection(self) -> "SessionConnection":
        from ._session_cxn_factory import get_session_cxn

        cxn_type = self._get_session_cxn_type()
        cxn = get_session_cxn(cxn_type, self)
        self.debug(f"Created session connection {cxn_type}")
        return cxn

    @abc.abstractmethod
    def _get_session_cxn_type(self) -> SessionCxnType:
        pass

    def on_state(self, callback: Callable[["Session", OpenState, str], None]) -> None:
        """
        On state callback

        Parameters
        ----------
        callback: Callable[[Session, OpenState, str], None]
            Callback function or method

        Raises
        ----------
        TypeError
            If user provided invalid object type
        """
        if not callable(callback):
            raise TypeError("Please provide callable object")

        self._on_state = callback

    def _call_on_state(self, message: str):
        if not self._on_state:
            return
        self.debug(f"Session calls on_state({self}, {self._state}, {message})")
        try:
            self._on_state(self, self._state, message)
        except Exception as e:
            self.error(
                f"on_state user function on session {self.session_id} raised error {e}"
            )

    def on_event(
        self, callback: Callable[["Session", EventCode, Union[dict, str]], None]
    ) -> None:
        """
        On event callback

        Parameters
        ----------
        callback: Callable[["Session", EventCode, Union[dict, str]], None]
            Callback function or method

        Raises
        ----------
        TypeError
            If user provided invalid object type
        """
        if not callable(callback):
            raise TypeError("Please provide callable object")

        self._on_event = callback

    def _call_on_event(self, event: EventCode, message: Union[dict, str]):
        if not self._on_event:
            return
        self.debug(f"Session calls on_event({self}, {event}, {message})")
        try:
            self._on_event(self, event, message)
        except Exception as e:
            self.error(
                f"on_event user function on session {self.session_id} raised error {e}"
            )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="session",
            content=f"{{name='{self.name}'}}",
        )

    def _on_config_updated(self):
        log_level = log.read_log_level_config()

        if log_level != self.get_log_level():
            self.set_log_level(log_level)

    @property
    def config(self) -> "_RDPConfig":
        return self._config

    @property
    def open_state(self):
        """
        Returns the session state.
        """
        return self._state

    @property
    def app_key(self):
        """
        Returns the application id.
        """
        return self._app_key

    @app_key.setter
    def app_key(self, app_key):
        """
        Set the application key.
        """
        from ...eikon._tools import is_string_type

        if app_key is None:
            return
        if not is_string_type(app_key):
            raise AttributeError("application key must be a string")

        self._app_key = app_key

    def update_access_token(self, access_token):
        DEBUG and self.debug(
            f"Session.update_access_token(access_token='{access_token}'"
        )
        self._access_token = access_token

        from ...delivery._stream import stream_cxn_cache

        if stream_cxn_cache.has_cxns(self):
            cxns_by_session = stream_cxn_cache.get_cxns(self)
            for cxn in cxns_by_session:
                cxn.send_login_message()

    @property
    def session_id(self):
        return self._session_id

    def logger(self) -> logging.Logger:
        return self._logger

    def _get_rdp_url_root(self) -> str:
        return ""

    @cached_property
    def http_request_timeout_secs(self):
        return self._http_service.request_timeout_secs

    ############################################################
    #   reconnection configuration

    @property
    def stream_auto_reconnection(self):
        return True

    @property
    def server_mode(self):
        return False

    @abc.abstractmethod
    def get_omm_login_message(self):
        """return the login message for OMM 'key' section"""
        pass

    @abc.abstractmethod
    def get_rdp_login_message(self, stream_id):
        """return the login message for RDP protocol"""
        pass

    ######################################
    # methods to manage log              #
    ######################################
    def set_log_level(self, log_level: [int, str]) -> None:
        """
        Set the log level.
        By default, logs are disabled.

        Parameters
        ----------
        log_level : int, str
            Possible values from logging module :
            [CRITICAL, FATAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET]
        """
        log_level = log.convert_log_level(log_level)
        self._logger.setLevel(log_level)

        if DEBUG:
            # Enable debugging

            # Report all mistakes managing asynchronous resources.
            warnings.simplefilter("always", ResourceWarning)

    def get_log_level(self):
        """
        Returns the log level
        """
        return self._logger.level

    def trace(self, message):
        self._logger.log(log.TRACE, message)

    ######################################
    # methods to open and close session  #
    ######################################
    def open(self) -> OpenState:
        """open session

        do an initialization config file, and http session if it's necessary.

        Returns
        -------
        OpenState
            the current state of this session.
        """
        if is_closed(self):
            self.debug(f"Open session")

            self._state = OpenState.Pending
            self._call_on_state("Session opening in progress")
            self._config.on(configure.ConfigEvent.UPDATE, self._on_config_updated)
            self._http_service.open()
            is_opened = self._connection.open()

            if is_opened:
                self._state = OpenState.Opened
                self._call_on_state("Session is opened")
            else:
                self.close()
                self._state = OpenState.Closed
                self._call_on_state(SESSION_IS_CLOSED)

            self.debug(f"Opened session")

        return self._state

    async def open_async(self) -> OpenState:
        """open session

        do an initialization config file, and http session if it's necessary.

        Returns
        -------
        OpenState
            the current state of this session.
        """
        if is_closed(self):
            self.debug(f"Open async session")

            self._state = OpenState.Pending
            self._call_on_state("Session opening in progress")
            self._config.on(configure.ConfigEvent.UPDATE, self._on_config_updated)
            await self._http_service.open_async()
            is_opened = self._connection.open()

            if is_opened:
                self._state = OpenState.Opened
                self._call_on_state("Session is opened")
            else:
                await self.close_async()
                self._state = OpenState.Closed
                self._call_on_state(SESSION_IS_CLOSED)

            self.debug(f"Opened async session")

        return self._state

    def close(self) -> OpenState:
        """
        Close platform/desktop session

        Returns
        -------
        OpenState
        """
        if not is_closed(self):
            self.debug(f"Close session")

            self._state = OpenState.Closed

            from ...delivery._stream import stream_cxn_cache

            stream_cxn_cache.close_cxns(self)
            self._http_service.close()
            self._connection.close()

            if DEBUG:
                import time
                from ...delivery._stream import stream_cxn_cache
                import threading

                time.sleep(5)
                s = "\n\t".join([str(t) for t in threading.enumerate()])
                self.debug(f"Threads:\n\t{s}")

                if stream_cxn_cache.has_cxns(self):
                    raise AssertionError(
                        f"Not all cxns are closed (session={self},\n"
                        f"cxns={stream_cxn_cache.get_cxns(self)})"
                    )

            self._config.remove_listener(
                configure.ConfigEvent.UPDATE, self._on_config_updated
            )
            self._call_on_state(SESSION_IS_CLOSED)
            self.debug(f"Closed session")

        return self._state

    async def close_async(self) -> OpenState:
        """
        Close platform/desktop session

        Returns
        -------
        OpenState
        """
        if not is_closed(self):
            self.debug(f"Close async session")

            self._state = OpenState.Closed

            from ...delivery._stream import stream_cxn_cache

            stream_cxn_cache.close_cxns(self)
            await self._http_service.close_async()
            self._connection.close()

            if DEBUG:
                from ...delivery._stream import stream_cxn_cache
                import threading

                await asyncio.sleep(5)
                s = "\n\t".join([str(t) for t in threading.enumerate()])
                self.debug(f"Threads:\n\t{s}")

                if stream_cxn_cache.has_cxns(self):
                    raise AssertionError(
                        f"Not all cxns are closed (session={self},\n"
                        f"cxns={stream_cxn_cache.get_cxns(self)})"
                    )

            self._config.remove_listener(
                configure.ConfigEvent.UPDATE, self._on_config_updated
            )
            self._call_on_state(SESSION_IS_CLOSED)
            self.debug(f"Closed async session")

        return self._state

    async def http_request_async(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        **kwargs,
    ):
        return await self._http_service.request_async(
            url=url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            json=json,
            closure=closure,
            **kwargs,
        )

    def http_request(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        **kwargs,
    ):
        response = self._http_service.request(
            url=url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            json=json,
            closure=closure,
            **kwargs,
        )
        return response
