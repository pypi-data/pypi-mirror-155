# coding: utf-8

from typing import TYPE_CHECKING

from ._session import Session
from .event_code import EventCode
from ._session_cxn_type import SessionCxnType
from ._session_type import SessionType
from ..._tools import create_repr, urljoin, cached_property, parse_url

if TYPE_CHECKING:
    from ._session_cxn_factory import PlatformConnection


class PlatformSession(Session):
    """
    This class is designed for handling the session to Refinitiv Data Platform (RDP)
    or Deployed Platform (TREP)
    - Refinitiv Data Platform are including handling an authentication and
        a token management (including refreshing token),
        also handling a real-time service discovery to get
        the service websocket endpoint and initialize the login for streaming
    - Deployed Platform is including the login for streaming
    """

    type = SessionType.PLATFORM

    def __init__(
        self,
        app_key=None,
        grant=None,
        signon_control=None,
        deployed_platform_host=None,
        deployed_platform_username=None,
        dacs_position=None,
        dacs_application_id=None,
        on_state=None,
        on_event=None,
        name="default",
        auto_reconnect=None,
        server_mode=None,
        base_url=None,
        auth_url=None,
        auth_authorize=None,
        auth_token=None,
        realtime_distribution_system_url=None,
    ):
        super().__init__(
            app_key,
            on_state=on_state,
            on_event=on_event,
            deployed_platform_username=deployed_platform_username,
            dacs_position=dacs_position,
            dacs_application_id=dacs_application_id,
            name=name,
        )

        self._grant = grant
        self._take_signon_control = signon_control if signon_control else True

        self._auto_reconnect = auto_reconnect
        self._server_mode = server_mode
        self._base_url = base_url
        self._auth_url = auth_url
        self._auth_authorize = auth_authorize
        self._auth_token = auth_token
        self._realtime_dist_system_url = realtime_distribution_system_url

        self._deployed_platform_host = deployed_platform_host
        self._deployed_platform_connection_name = self.name

        if self._deployed_platform_host is None and self._realtime_dist_system_url:
            parse_result = parse_url(self._realtime_dist_system_url)
            self._deployed_platform_host = parse_result.netloc
            self.debug(
                f"Using the Refinitiv realtime distribution system : "
                f"url at {self._realtime_dist_system_url},\n"
                f"deployed_platform_host={self._deployed_platform_host}"
            )

        elif self._deployed_platform_host and not self._realtime_dist_system_url:
            self.debug(
                f"Using the specific "
                f"deployed_platform_host={self._deployed_platform_host}"
            )

        elif self._deployed_platform_host and self._realtime_dist_system_url:
            # what to do ?
            pass

    @property
    def stream_auto_reconnection(self):
        return self._auto_reconnect

    @property
    def server_mode(self):
        return self._server_mode

    @property
    def signon_control(self):
        return self._take_signon_control

    @property
    def authentication_token_endpoint_url(self) -> str:
        url = urljoin(
            self._get_rdp_url_root() or "", self._auth_url or "", self._auth_token or ""
        )
        return url

    @cached_property
    def _connection(self) -> "PlatformConnection":
        from ._session_cxn_factory import get_session_cxn

        cxn_type = self._get_session_cxn_type()
        cxn = get_session_cxn(cxn_type, self)

        if cxn_type is SessionCxnType.REFINITIV_DATA:
            from .event import UpdateEvent

            auth_manager = cxn.auth_manager
            auth_manager.on(
                UpdateEvent.AUTHENTICATION_SUCCESS,
                lambda message: self._call_on_event(
                    EventCode.SessionAuthenticationSuccess, message
                ),
            )
            auth_manager.on(
                UpdateEvent.AUTHENTICATION_FAILED,
                lambda message: self._call_on_event(
                    EventCode.SessionAuthenticationFailed, message
                ),
            )
            auth_manager.on(
                UpdateEvent.RECONNECTING,
                lambda message: self._call_on_event(
                    EventCode.SessionReconnecting, "Session is reconnecting"
                ),
            )
            auth_manager.on(UpdateEvent.UPDATE_ACCESS_TOKEN, self.update_access_token)

        self.debug(f"Created session connection {cxn_type}")
        return cxn

    def _get_session_cxn_type(self) -> SessionCxnType:
        if self._grant and self._grant.is_valid() and self._deployed_platform_host:
            cxn_type = SessionCxnType.REFINITIV_DATA_AND_DEPLOYED

        elif self._grant and self._grant.is_valid():
            cxn_type = SessionCxnType.REFINITIV_DATA

        elif self._deployed_platform_host:
            cxn_type = SessionCxnType.DEPLOYED

        else:
            raise AttributeError(f"Can't get a session connection type")

        return cxn_type

    def _get_rdp_url_root(self):
        return self._base_url

    def _get_auth_token_uri(self):
        auth_token_uri = urljoin(self._auth_url, self._auth_token)
        uri = urljoin(self._get_rdp_url_root(), auth_token_uri)
        return uri

    def get_omm_login_message(self):
        return self._connection.get_omm_login_message()

    def get_rdp_login_message(self, stream_id):
        return {
            "streamID": f"{stream_id:d}",
            "method": "Auth",
            "token": self._access_token,
        }

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
        return await self._connection.http_request_async(
            url,
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
        return self._connection.http_request(
            url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            json=json,
            closure=closure,
            **kwargs,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="session.platform",
            content=f"{{session_name='{self.name}'}}",
        )

    def __str__(self) -> str:
        s = (
            f"{self.__class__.__name__} {{\n"
            f"\t\tname={self.name},\n"
            f"\t\tserver_mode={self.server_mode},\n"
            f"\t\tstream_auto_reconnection={self.stream_auto_reconnection},\n"
            f"\t\tsignon_control={self.signon_control},\n"
            f"\t\tauthentication_token_endpoint_url={self.authentication_token_endpoint_url}}}"
        )
        return s
