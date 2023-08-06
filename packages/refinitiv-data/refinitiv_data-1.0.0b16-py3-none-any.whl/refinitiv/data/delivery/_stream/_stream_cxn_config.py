import abc
import collections
import json
import os
import pathlib
from typing import List, Optional, TYPE_CHECKING, Union

from .proxy_info import ProxyInfo
from ..._configure import keys
from ..._core.session import SessionType
from ..._core.session._session_cxn_type import SessionCxnType
from ..._tools import parse_url, urljoin
from ...errors import RDError

if TYPE_CHECKING:
    from ..._core.session import Session, PlatformSession
    from ..._configure import _RDPConfig

StreamServiceInfo = collections.namedtuple(
    "StreamServiceInfo",
    ["scheme", "host", "port", "path", "data_formats", "location", "transport"],
)

_DEFAULT_RECONNECTION_DELAY_SECS = 5


class StreamCxnConfig(abc.ABC):
    def __init__(
        self,
        infos: Union[List["StreamServiceInfo"], "StreamServiceInfo"],
        protocols: Union[List[str], str],
        transport: str = "websocket",
    ):
        if isinstance(infos, list) and len(infos) == 0:
            raise ValueError("infos are empty")

        if not isinstance(infos, list):
            infos = [infos]

        if not isinstance(protocols, list):
            protocols = [protocols]

        self._infos = infos
        self._protocols = protocols
        self._transport = transport
        self._index = 0

    @property
    def transport(self):
        return self._transport

    @property
    def info(self):
        return self._infos[self._index]

    @property
    def url(self):
        return self._get_url(self.info)

    @property
    def url_scheme(self):
        return self.info.scheme

    @property
    def urls(self):
        return [self._get_url(info) for info in self._infos]

    @property
    def headers(self):
        return []

    @property
    def data_formats(self):
        return self.info.data_formats

    @property
    def supported_protocols(self):
        return self._protocols

    def reset_reconnection_config(self):
        self._index = 0

    @property
    def no_proxy(self):
        return ProxyInfo.get_no_proxy()

    @property
    def proxy_config(self):
        proxies_info = ProxyInfo.get_proxies_info()
        if self.url_scheme == "wss":
            # try to get https proxy then http proxy if https not configured
            return proxies_info.get("https", proxies_info.get("http", None))
        else:
            return proxies_info.get("http", None)

    @property
    def data_fmt(self):
        if not self.data_formats:
            return ""
        return self.data_formats[0]

    @property
    def delay(self):
        return self._index * _DEFAULT_RECONNECTION_DELAY_SECS

    def set_next_url(self):
        self._index = (self._index + 1) % len(self._infos)

    @abc.abstractmethod
    def _get_url(self, info: "StreamServiceInfo") -> str:
        pass

    def __str__(self) -> str:
        urls = "\n\t\t\t ".join(self.urls)
        s = (
            f"{self.__class__.__name__} {{\n"
            f"\t\tinfo={self.info},\n"
            f"\t\turl={self.url},\n"
            f"\t\turl_scheme={self.url_scheme},\n"
            f"\t\turls={urls},\n"
            f"\t\theaders={self.headers}, "
            f"data_formats={self.data_formats}, "
            f"supported_protocols={self.supported_protocols}, "
            f"no_proxy={self.no_proxy}, "
            f"proxy_config={self.proxy_config}, "
            f"data_fmt={self.data_fmt}, "
            f"delay={self.delay}}}"
        )
        return s


class DesktopStreamCxnConfig(StreamCxnConfig):
    def __init__(
        self,
        session: "Session",
        infos: Union[List["StreamServiceInfo"], "StreamServiceInfo"],
        protocols: Union[List[str], str],
    ):
        super().__init__(infos, protocols)
        self._session = session

    @property
    def headers(self):
        app_version = os.getenv("DP_PROXY_APP_VERSION")
        headers = [f"x-tr-applicationid: {self._session.app_key}"]

        if self._session._access_token:
            headers.append(f"Authorization: Bearer {self._session._access_token}")

        if app_version and self._session.type == SessionType.DESKTOP:
            headers.append(f"app-version: {app_version}")

        return headers

    def _get_url(self, info: "StreamServiceInfo") -> str:
        return f"{info.scheme}://{info.host}:{info.port}/{info.path}"


class PlatformStreamCxnConfig(StreamCxnConfig):
    def _get_url(self, info: "StreamServiceInfo") -> str:
        if self.transport == "tcp":
            return f"{info.host}:{info.port}"
        else:
            path = info.path or "WebSocket"
            return f"{info.scheme}://{info.host}:{info.port}/{path}"


class NullStreamCxnConfig(StreamCxnConfig):
    def __init__(self):
        StreamCxnConfig.__init__(
            self, [StreamServiceInfo("", "", "", "", "", "", "")], []
        )

    def _get_url(self, info):
        return ""


def get_discovery_url(
    root_url: str, streaming_name: str, endpoint_name: str, config: "_RDPConfig"
) -> str:
    config_name = f"apis.streaming.{streaming_name}"
    config_endpoint_name = f"{config_name}.endpoints.{endpoint_name}"
    base_path = config.get_str(f"{config_name}.url")

    try:
        endpoint_path = config.get_str(f"{config_endpoint_name}.path")
    except KeyError:
        raise KeyError(
            f"Cannot find discovery endpoint '{endpoint_name}' "
            f"for streaming '{streaming_name}' in config."
        )

    if base_path.startswith("http"):
        url = base_path
    else:
        url = urljoin(root_url, base_path)

    return urljoin(url, endpoint_path)


def _filter_by_location(locations: List[str], infos: List[StreamServiceInfo]) -> list:
    if not locations:
        return infos

    filtered = []
    for location in locations:
        for info in infos:
            has_location = any(
                loc.strip().startswith(location) for loc in info.location
            )
            if has_location and info not in filtered:
                filtered.append(info)

    return filtered


class CxnConfigProvider(abc.ABC):
    config_class = None
    _port_by_prefix = {
        80: "ws",
        443: "wss",
    }

    def get_cfg(
        self, session: "Session", api_cfg_key: str
    ) -> Union[PlatformStreamCxnConfig, DesktopStreamCxnConfig]:
        """
        Parameters
        ----------
        session: Session
        api_cfg_key: str
            Example - "streaming/pricing/main"

        Returns
        -------
        PlatformStreamCxnConfig or DesktopStreamCxnConfig

        """
        _, content_name, endpoint_name = api_cfg_key.split("/")
        cfg: "_RDPConfig" = session.config
        url: Optional[str] = None

        if cfg.get(f"apis.streaming.{content_name}.use_rwf", False):
            transport = "tcp"
        else:
            transport = "websocket"

        if transport == "websocket":
            url = cfg.get(keys.get_stream_websocket_url(content_name, endpoint_name))
        if transport == "tcp" or (transport == "websocket" and url is None):
            url = cfg.get(keys.get_stream_direct_url(content_name, endpoint_name))

        if url is not None:
            infos = [self.info_from_url(transport, url)]

        else:
            url_root: str = session._get_rdp_url_root()
            discovery_url: str = get_discovery_url(
                url_root, content_name, endpoint_name, cfg
            )
            infos = self._request_infos(
                discovery_url, api_cfg_key, cfg, session, transport
            )
        protocols = cfg.get_list(keys.stream_protocols(content_name, endpoint_name))
        return self._create_cfg(session, infos, protocols, transport)

    @staticmethod
    def info_from_url(transport: str, url: str, data_formats=None) -> StreamServiceInfo:
        if data_formats is None:
            data_formats = ["unknown"]

        # If there is no scheme or netloc add netloc marker to make it valid URL
        if not ("://" in url or url.startswith("//")) and not url.startswith("/"):
            url = "//" + url

        result = parse_url(url)
        scheme = result.scheme
        host = result.hostname
        port = result.port
        path = result.path

        # If url parsing did not get valid hostname, raise exception
        if not host:
            raise ValueError(f"Invalid URL: {url}")

        if not scheme and transport == "websocket":
            scheme = "wss" if port == 443 else "ws"
        return StreamServiceInfo(
            scheme=scheme or "",
            host=host or "",
            port=port or 80,
            path=path or "",
            data_formats=data_formats,
            location="",
            transport=transport,
        )

    def _request_infos(
        self,
        discovery_url: str,
        api_config_key: str,
        config: "_RDPConfig",
        session: "Session",
        transport: str = "websocket",
    ) -> List[StreamServiceInfo]:

        content_name = api_config_key.split("/")[1]
        tier: Optional[int] = config.get(f"apis.streaming.{content_name}.tier")

        response = session.http_request(
            discovery_url,
            # server won't accept tier: false
            params={"tier": True} if tier else {},
        )
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            raise RuntimeError(f"Cannot load config from {discovery_url}, {response}")

        err = data.get("error")
        if err:
            raise RDError(response.status_code, err.get("message"))

        infos = []
        for service in data.get("services", []):
            if service.get("transport") != transport:
                continue

            if tier is not None and "tier" in service:
                tier_range: List[int] = service["tier"]
                if tier < tier_range[0] or tier > tier_range[1]:
                    continue

            endpoint_path = pathlib.Path(service.get("endpoint"))
            host = str(endpoint_path.parts[0])
            path = "/".join(endpoint_path.parts[1:])

            scheme = ""
            port = service.get("port")
            if transport == "websocket":
                scheme = self._port_by_prefix.get(port, "ws")

            infos.append(
                StreamServiceInfo(
                    scheme=scheme,
                    host=host,
                    port=port,
                    path=path,
                    data_formats=service.get("dataFormat", ["unknown"]),
                    location=service.get("location"),
                    transport=transport,
                )
            )

        return self._filter_infos(infos, api_config_key, config)

    def _filter_infos(
        self,
        infos: List[StreamServiceInfo],
        api_cfg_key: str,
        cfg: "_RDPConfig",
    ) -> List[StreamServiceInfo]:
        return infos

    def _create_cfg(
        self,
        session: "Session",
        infos: List[StreamServiceInfo],
        protocols: List[str],
        transport: str = "websocket",
    ) -> Union[PlatformStreamCxnConfig, DesktopStreamCxnConfig]:
        return self.config_class(infos, protocols, transport)


class DesktopCxnConfigProvider(CxnConfigProvider):
    config_class = DesktopStreamCxnConfig

    def _create_cfg(
        self,
        session: "Session",
        infos: List[StreamServiceInfo],
        protocols: List[str],
        transport: str = "websocket",
    ) -> Union[PlatformStreamCxnConfig, DesktopStreamCxnConfig]:
        return self.config_class(session, infos, protocols)


class PlatformCxnConfigProvider(CxnConfigProvider):
    config_class = PlatformStreamCxnConfig

    def _filter_infos(
        self,
        infos: List[StreamServiceInfo],
        api_cfg_key: str,
        cfg: "_RDPConfig",
    ) -> List[StreamServiceInfo]:
        _, content_name, endpoint_name = api_cfg_key.split("/")

        locations = cfg.get_list(
            keys.stream_connects_locations(content_name, endpoint_name)
        )
        return _filter_by_location(locations, infos)


class DeployedCxnConfigProvider(CxnConfigProvider):
    def get_cfg(
        self, session: "PlatformSession", api_cfg_key: str
    ) -> PlatformStreamCxnConfig:

        url: str = session._deployed_platform_host
        cfg: "_RDPConfig" = session.config
        _, content_name, endpoint_name = api_cfg_key.split("/")

        if url is None:
            session_name: str = session.name
            key = keys.platform_realtime_distribution_system(session_name)
            url_key = f"{key}.url"
            url = cfg.get_str(url_key)

        if cfg.get(f"apis.streaming.{content_name}.use_rwf", False):
            transport = "tcp"
            data_formats = None
        else:
            transport = "websocket"
            data_formats = ["tr_json2"]

        info = self.info_from_url(transport, url, data_formats=data_formats)

        return PlatformStreamCxnConfig(info, "OMM", transport=transport)


class PlatformAndDeployedCxnConfigProvider(
    DeployedCxnConfigProvider, PlatformCxnConfigProvider
):
    def get_cfg(self, session: "PlatformSession", api_cfg_key: str) -> StreamCxnConfig:

        if api_cfg_key.startswith("streaming/pricing/main"):
            cxn_config = DeployedCxnConfigProvider.get_cfg(self, session, api_cfg_key)
        else:
            cxn_config = PlatformCxnConfigProvider.get_cfg(self, session, api_cfg_key)

        return cxn_config


cxn_cfg_provider_by_session_cxn_type = {
    SessionCxnType.DEPLOYED: DeployedCxnConfigProvider(),
    SessionCxnType.REFINITIV_DATA: PlatformCxnConfigProvider(),
    SessionCxnType.REFINITIV_DATA_AND_DEPLOYED: PlatformAndDeployedCxnConfigProvider(),
    SessionCxnType.DESKTOP: DesktopCxnConfigProvider(),
}


def get_cxn_config(api_config_key: str, session: "Session") -> StreamCxnConfig:
    session_cxn_type = session._get_session_cxn_type()
    cxn_cfg_provider = cxn_cfg_provider_by_session_cxn_type.get(session_cxn_type)

    if not cxn_cfg_provider:
        raise ValueError(
            f"Can't find cxn_cfg_provider by session_cxn_type={session_cxn_type}"
        )

    return cxn_cfg_provider.get_cfg(session, api_config_key)
