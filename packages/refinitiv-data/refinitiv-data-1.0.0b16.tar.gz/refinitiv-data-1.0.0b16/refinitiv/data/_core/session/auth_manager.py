import threading
import time
from typing import TYPE_CHECKING, Optional, Union, Callable

from pyee import EventEmitter

from ._default_session_manager import Wrapper
from .access_token_updater import AccessTokenUpdater
from .event import UpdateEvent
from .refresh_token_updater import RefreshTokenUpdater
from .tools import MINUTES_10, get_delays
from ..log_reporter import LogReporter
from ..._tools import cached_property

if TYPE_CHECKING:
    from ._platform_session import PlatformSession

DEFAULT_EXPIRES_IN_SEC = MINUTES_10
DEFAULT_LATENCY_SEC = 20

delays = get_delays()


class TokenInfo:
    def __init__(
        self,
        access_token: str,
        expires_in: Union[float, str, int],
        scope: Optional[str] = "",
        token_type: Optional[str] = "",
        refresh_token: Optional[str] = "",
    ) -> None:
        super().__init__()
        self.token_type = token_type
        self.scope = scope
        self.refresh_token = refresh_token

        try:
            expires_in = float(expires_in)
            if expires_in < DEFAULT_EXPIRES_IN_SEC:
                expires_in = DEFAULT_EXPIRES_IN_SEC
        except Exception:
            expires_in = DEFAULT_EXPIRES_IN_SEC

        self.expires_in = float(expires_in)
        self.expires_at = time.time() + expires_in

        self.access_token = access_token

    def calc_expires_in(self, latency: float) -> int:
        if latency > DEFAULT_LATENCY_SEC:
            latency = DEFAULT_LATENCY_SEC

        expires_secs = self.expires_in // 2

        if expires_secs - latency > 0:
            expires_secs = expires_secs - latency

        return int(expires_secs)


def create_token_info(json_content: dict) -> TokenInfo:
    token_info = TokenInfo(
        access_token=json_content["access_token"],
        refresh_token=json_content["refresh_token"],
        expires_in=json_content.get("expires_in", ""),
        scope=json_content.get("scope", ""),
        token_type=json_content.get("token_type", ""),
    )
    return token_info


class AuthManager(LogReporter):
    """
    Methods
    -------
    is_closed()
        The method returns True if closed, otherwise False

    is_authorized()
        The method returns True if authorized, otherwise False.
        If instance destroyed or closed always returns False

    authorize()
        The method starts process authorization

    close()
        The method stops refresh token updater and access token updater

    dispose()
        The method destroy an instance

    """

    def __init__(self, session: "PlatformSession", auto_reconnect: bool) -> None:
        LogReporter.__init__(self, logger=session)

        self._session = session
        self._auto_reconnect = auto_reconnect

        self._ee: EventEmitter = EventEmitter()
        self._token_info: Wrapper = Wrapper[TokenInfo]()

        self._closed: bool = False
        self._authorized: bool = False
        self._disposed: bool = False

        self._result_evt: threading.Event = threading.Event()
        self._start_evt: threading.Event = threading.Event()
        self._thread: threading.Thread = threading.Thread(
            target=self._do_authorize,
            name="AuthManager-Thread",
            daemon=True,
        )

    @cached_property
    def _access_token_updater(self) -> AccessTokenUpdater:
        return AccessTokenUpdater(
            self._session,
            0.00001,
            self._access_token_update_handler,
        )

    @cached_property
    def _refresh_token_updater(self) -> RefreshTokenUpdater:
        return RefreshTokenUpdater(
            self._session,
            self._token_info,
            0.00001,
            self._refresh_token_update_handler,
        )

    def on(self, event: str, listener: Callable):
        self._ee.on(event, listener)

    def is_closed(self) -> bool:
        """

        Returns
        -------
        bool
            True if closed, otherwise False
        """
        return self._closed is True

    def is_authorized(self) -> bool:
        """

        Returns
        -------
        bool
            True if authorized, otherwise False
        """
        if self.is_closed():
            return False

        return self._authorized is True

    def authorize(self) -> bool:
        """
        The method starts process authorization

        Returns
        -------
        bool
            True if authorized, otherwise False
        """
        if self._disposed:
            raise RuntimeError("AuthManager disposed")

        if self.is_authorized():
            return True

        self.debug("AuthManager: start authorize")

        self._closed = False
        self._authorized = False

        self._result_evt.clear()
        self._start_evt.set()

        if not self._thread.ident:
            self._thread.start()

        self._result_evt.wait()

        is_authorized = self.is_authorized()
        self.debug(f"AuthManager: end authorize, result {is_authorized}")
        return is_authorized

    def _do_authorize(self):
        while not self._disposed:

            self._start_evt.wait()

            if self._disposed:
                break

            self.debug(
                f"AuthManager: Access token will be requested "
                f"in {self._access_token_updater.delay} seconds"
            )
            self._access_token_updater.start()

            if self.is_authorized():
                latency_secs = self._access_token_updater.latency_secs
                delay = self._token_info.get().calc_expires_in(latency_secs)
                self._refresh_token_updater.delay = delay
                self.debug(
                    f"AuthManager: Refresh token will be requested "
                    f"in {self._refresh_token_updater.delay} seconds"
                )
                self._refresh_token_updater.start()

    def close(self):
        """
        The method stops refresh token updater and access token updater

        Returns
        -------
        None
        """
        if self._disposed:
            raise RuntimeError("AuthManager disposed")

        if self.is_closed():
            return

        self.debug("AuthManager: close")
        self._start_evt.clear()
        self._access_token_updater.stop()
        self._refresh_token_updater.stop()
        self._closed = True
        self._authorized = False

    def _access_token_update_handler(
        self, event: str, message: str, json_content: dict
    ) -> None:
        self.debug(
            f"AuthManager: Access token handler, event: {event}, message: {message}"
        )

        if event is UpdateEvent.ACCESS_TOKEN_SUCCESS:
            self._authorized = True
            delays.reset()
            token_info = create_token_info(json_content)
            self._token_info.set(token_info)
            access_token = token_info.access_token
            self.debug(
                f"Access token {access_token}. "
                f"Expire in {token_info.expires_in} seconds"
            )
            self._ee.emit(UpdateEvent.UPDATE_ACCESS_TOKEN, access_token)
            self._access_token_updater.stop()
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_SUCCESS, message)
            self._result_evt.set()

        elif event is UpdateEvent.ACCESS_TOKEN_UNAUTHORIZED:
            self._authorized = False
            self._access_token_updater.stop()
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)
            self.close()
            self._result_evt.set()

        elif event is UpdateEvent.ACCESS_TOKEN_FAILED:
            if not self._auto_reconnect:
                self._authorized = False
                self._access_token_updater.stop()
                self._result_evt.set()

            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)

            if self._auto_reconnect:
                delay = delays.next()
                self.debug(f"AuthManager: reconnecting in {delay} secs")
                self._access_token_updater.delay = delay
                self._ee.emit(UpdateEvent.RECONNECTING, message)

            else:
                self.close()

    def _refresh_token_update_handler(
        self, event: str, message: str, json_content: dict
    ) -> None:
        self.debug(
            f"AuthManager: Refresh token handler, event: {event}, message: {message}"
        )

        if event is UpdateEvent.REFRESH_TOKEN_SUCCESS:
            token_info = create_token_info(json_content)
            self._token_info.set(token_info)
            access_token = token_info.access_token
            self.debug(
                f"Received access token {token_info.refresh_token}. "
                f"Expire in {token_info.expires_in} seconds"
            )
            self._ee.emit(UpdateEvent.UPDATE_ACCESS_TOKEN, access_token)
            latency_secs = self._access_token_updater.latency_secs
            delay = token_info.calc_expires_in(latency_secs)
            self._refresh_token_updater.delay = delay
            self.debug(f"Set refresh token delay to {delay} seconds")
            self._ee.emit(event, message)

        elif event is UpdateEvent.REFRESH_TOKEN_BAD:
            self._authorized = False
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)
            self.close()

        elif event is UpdateEvent.REFRESH_TOKEN_FAILED:
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)

            if self._auto_reconnect:
                delay = delays.next()
                self.debug(
                    f"AuthManager: Trying to get Refresh token again in {delay} secs"
                )
                self._refresh_token_updater.delay = delay
                self._ee.emit(UpdateEvent.RECONNECTING, message)

            else:
                self._authorized = False
                self.close()

        elif event is UpdateEvent.REFRESH_TOKEN_EXPIRED:
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)
            self._authorized = False

            if self._auto_reconnect:
                self.debug("AuthManager: reconnecting")
                self._ee.emit(UpdateEvent.RECONNECTING, message)
                self._refresh_token_updater.stop()

            else:
                self.close()

    def dispose(self):
        """
        The method destroy an instance

        Returns
        -------
        None
        """
        if self._disposed:
            return

        if not self.is_closed():
            self.close()

        self._disposed = True
        self._access_token_updater.dispose()
        self._refresh_token_updater.dispose()
        self._start_evt.set()
        self._ee.remove_all_listeners()
        self._ee = None
        self._token_info = None
        self._start_evt = None
        self._thread = None
        self._session = None
