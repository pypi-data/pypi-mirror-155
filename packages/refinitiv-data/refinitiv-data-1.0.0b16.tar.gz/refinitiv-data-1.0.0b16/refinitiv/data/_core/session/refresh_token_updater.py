import time
from typing import Callable, TYPE_CHECKING, Union

import requests

from .event import UpdateEvent
from .tools import NullResponse, UNAUTHORIZED_CODES
from .updater import Updater
from ..log_reporter import LogReporter

if TYPE_CHECKING:
    from .auth_manager import TokenInfo
    from ._default_session_manager import Wrapper
    from ._platform_session import PlatformSession
    from .grant_password import GrantPassword

codes = requests.codes


class RefreshTokenUpdater(Updater, LogReporter):
    def __init__(
        self,
        session: "PlatformSession",
        token_info: "Wrapper",
        delay: Union[int, float],
        callback: Callable[[str, str, dict], None],
    ) -> None:
        Updater.__init__(self, delay, "RefreshTokenUpdater")
        LogReporter.__init__(self, logger=session)

        self._session = session
        self._token_info = token_info
        self._callback = callback
        self._grant: "GrantPassword" = self._session._grant
        self._app_key = self._session._app_key
        self._url = self._session.authentication_token_endpoint_url

    @Updater.delay.setter
    def delay(self, value: int):
        if value <= 0:
            raise ValueError("Delay must be greater than 0")
        Updater.delay.fset(self, value)

    def _do_update(self):
        cur_time = time.time()

        if self._token_info.get().expires_at <= cur_time:
            event = UpdateEvent.REFRESH_TOKEN_EXPIRED
            message = "Time expired for the refresh token update"
            self.debug(message)
            self._callback(event, message, {})
            return

        response = self._request_token(
            self._grant, self._token_info.get(), self._app_key, self._url
        )

        status_code = response.status_code
        json_content = response.json()

        if status_code == codes.ok:
            event = UpdateEvent.REFRESH_TOKEN_SUCCESS
            message = "All is well"

        elif status_code in UNAUTHORIZED_CODES:
            event = UpdateEvent.REFRESH_TOKEN_BAD
            error = json_content.get("error")
            error_description = json_content.get(
                "error_description", "empty error description"
            )
            message = error_description
            self.error(f"[Error {status_code} - {error}] {error_description}")

        else:
            event = UpdateEvent.REFRESH_TOKEN_FAILED
            error = json_content.get("error")
            error_description = json_content.get(
                "error_description",
                getattr(response, "text", "empty error description"),
            )
            message = error_description
            self.error(f"[Error {status_code} - {error}] {error_description}")

        self._callback(event, message, json_content)

    def _request_token(
        self,
        grant: "GrantPassword",
        token_info: "TokenInfo",
        app_key: str,
        url: str,
    ):
        data = {
            "client_id": app_key,
            "grant_type": "refresh_token",
            "username": grant.get_username(),
            "refresh_token": token_info.refresh_token,
        }
        self.debug(f"Request refresh token to {url}\n\twith post data = {str(data)}")
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token_info.access_token}",
        }
        try:
            response = self._session.http_request(
                url=url, method="POST", headers=headers, data=data, auto_retry=True
            )
            self.debug(f"Refresh token response: {response.text}")
        except Exception as e:
            response = NullResponse()
            response.text = str(e)

        return response

    def _do_dispose(self):
        self._session = None
        self._callback = None
