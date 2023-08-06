import time
from typing import TYPE_CHECKING, Callable

import requests

from .event import UpdateEvent
from .tools import NullResponse, UNAUTHORIZED_CODES
from .updater import Updater
from ..log_reporter import LogReporter

if TYPE_CHECKING:
    from ._platform_session import PlatformSession
    from .grant_password import GrantPassword

codes = requests.codes


class AccessTokenUpdater(Updater, LogReporter):
    def __init__(
        self,
        session: "PlatformSession",
        delay: int,
        callback: Callable[[str, str, dict], None],
    ):
        Updater.__init__(self, delay, "AccessTokenUpdater")
        LogReporter.__init__(self, logger=session)

        self._session = session
        self._callback = callback

        self._grant: "GrantPassword" = self._session._grant
        self._app_key: str = self._session._app_key
        self._url: str = self._session.authentication_token_endpoint_url
        self._signon_control: bool = self._session.signon_control

        self.latency_secs: float = 0.0

    @Updater.delay.setter
    def delay(self, value: int):
        if value <= 0:
            raise ValueError("Delay must be greater than 0")
        Updater.delay.fset(self, value)

    def _do_update(self):
        response = self._request_token(
            self._grant, self._app_key, self._url, self._signon_control
        )
        status_code = response.status_code
        json_content = response.json()

        if status_code == codes.ok:
            event = UpdateEvent.ACCESS_TOKEN_SUCCESS
            message = "All is well"

        elif status_code in UNAUTHORIZED_CODES:
            event = UpdateEvent.ACCESS_TOKEN_UNAUTHORIZED
            error = json_content.get("error", "empty error")
            error_description = json_content.get(
                "error_description", "empty error description"
            )
            message = error_description
            self.error(f"[Error {status_code} - {error}] {error_description}")

        else:
            event = UpdateEvent.ACCESS_TOKEN_FAILED
            error = json_content.get("error")
            error_description = json_content.get(
                "error_description",
                getattr(response, "text", "empty error description"),
            )
            message = error_description
            self.error(f"[Error {status_code} - {error}] {error_description}")

        self._callback(event, message, json_content)

    def _request_token(
        self, grant: "GrantPassword", app_key: str, url: str, take_signon_control: bool
    ):
        username = grant.get_username()
        data = {
            "scope": grant.get_token_scope(),
            "grant_type": "password",
            "username": username,
            "password": grant.get_password(),
            "takeExclusiveSignOnControl": "true" if take_signon_control else "false",
        }

        if app_key is not None:
            data["client_id"] = app_key

        self.debug(
            f"Request access token to {url}\n"
            f"\twith post data {str(data)}\n"
            f"\twith auth {username}"
        )
        headers = {"Accept": "application/json"}
        try:
            start = time.time()
            response = self._session.http_request(
                url=url,
                method="POST",
                headers=headers,
                data=data,
            )
            end = time.time()
            self.latency_secs = end - start
            self.debug(
                f"Latency: {self.latency_secs} sec.\n"
                f"Access token response: {response.text}"
            )
        except Exception as e:
            response = NullResponse()
            response.text = str(e)

        return response

    def _do_dispose(self):
        self._session = None
        self._callback = None
