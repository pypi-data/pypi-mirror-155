import os
from typing import Optional, TYPE_CHECKING, Union

import httpx

from . import SessionType
from ._retry_transport import RequestRetryException, RetryAsyncTransport, RetryTransport
from ..log_reporter import LogReporter
from ... import _configure as configure
from ..._tools import cached_property

APPLICATION_JSON = "application/json"

if TYPE_CHECKING:
    from ._session import Session


def get_http_limits(config):
    max_connections = config.get(configure.keys.http_max_connections)
    max_keepalive_connections = config.get(
        configure.keys.http_max_keepalive_connections
    )
    limits = httpx.Limits(
        max_connections=max_connections,
        max_keepalive_connections=max_keepalive_connections,
    )
    return limits


def get_http_request_timeout_secs(session):
    """the default http request timeout in secs"""
    key = configure.keys.http_request_timeout
    value = session.config.get(key)

    is_list = isinstance(value, list)
    if is_list and len(value) == 1:
        value = value[0]
        try:
            value = int(value)
        except ValueError:
            pass

    number = isinstance(value, int) or isinstance(value, float)
    negative_number = number and value < 0

    if number and value == 0:
        value = None
    elif number and value == 1:
        value = 1

    is_none = value is None

    set_default = not is_none and (not number or negative_number)

    if set_default:
        value = configure.defaults.http_request_timeout
        session.warning(f"Invalid value of the {key}. Default value is used")

    return value


class BaseHTTPClient(LogReporter):
    def __init__(self, session: "Session") -> None:
        super().__init__(session)
        self._session: "Session" = session

        self._client: Optional[httpx.Client, httpx.AsyncClient] = None
        self._auto_retry_client: Optional[httpx.Client, httpx.AsyncClient] = None

    def is_closed(self) -> bool:
        is_closed = self._client is None
        return is_closed or self._client.is_closed

    def _filtered_timeout(self, kwargs):
        http_request_timeout = None
        if httpx.__version__ < "0.20.0":
            http_request_timeout = kwargs.pop(
                "timeout", get_http_request_timeout_secs(self._session)
            )
        else:
            if "timeout" not in kwargs:
                #   override using the http request timeout from config file
                kwargs["timeout"] = get_http_request_timeout_secs(self._session)
        return http_request_timeout

    def build_request(
        self,
        client: Union[httpx.AsyncClient, httpx.Client],
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        **kwargs,
    ) -> httpx.Request:
        if method is None:
            method = "GET"

        if headers is None:
            headers = {}

        access_token = self._session._access_token
        app_key = self._session.app_key

        if access_token is not None:
            headers["Authorization"] = "Bearer {}".format(access_token)

        if closure is not None:
            headers["Closure"] = closure

        cookies = None

        if self._session.type == SessionType.DESKTOP:
            proxy_app_version = os.getenv("DP_PROXY_APP_VERSION")
            user_uuid = os.getenv("REFINITIV_AAA_USER_ID")

            if proxy_app_version:
                headers.update({"app-version": proxy_app_version})

            if user_uuid:
                cookies = {"user_uuid": user_uuid}

        headers.update({"x-tr-applicationid": app_key})

        if httpx.__version__ < "0.20.0":
            kwargs.pop("timeout", None)

        self.debug(
            f"Request to {url}\n"
            f"\tmethod = {method}\n"
            f"\theaders = {headers}\n"
            f"\tparams = {params}\n"
            f"\tcookies = {cookies}\n"
            f"\tdata = {data}\n"
            f"\tjson = {json}"
        )
        request = client.build_request(
            method=method,
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            **kwargs,
        )
        return request


class HTTPClient(BaseHTTPClient):
    def open(self):
        config = self._session.config
        limits = get_http_limits(config)

        # httpx has its default Accept header and
        # server wants application/json or nothing
        self._client = httpx.Client(headers={"Accept": APPLICATION_JSON}, limits=limits)

        key = configure.keys.http_auto_retry_config
        auto_retry_config = config.get(key, None)

        if auto_retry_config:
            number_of_retries = auto_retry_config.get("number-of-retries", 3)
            retry_on_errors = auto_retry_config.get("on-errors", [])
            retry_backoff_factor = auto_retry_config.get("backoff-factor", 1)
            retry_on_methods = auto_retry_config.get("on-methods", ["GET", "POST"])

            retry_transport = RetryTransport(
                total_attempts=number_of_retries,
                on_statuses=retry_on_errors,
                on_methods=retry_on_methods,
                backoff_factor=retry_backoff_factor,
            )
            self._auto_retry_client = httpx.Client(transport=retry_transport)

    def close(self):
        if self._client:
            self._client.close()
            self._client = None

        if self._auto_retry_client:
            self._auto_retry_client.close()
            self._auto_retry_client = None

    def send(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        **kwargs,
    ) -> httpx.Response:
        auto_retry = kwargs.pop("auto_retry", False)
        client: httpx.Client = self._auto_retry_client if auto_retry else self._client

        http_request_timeout = self._filtered_timeout(kwargs=kwargs)

        request = self.build_request(
            client=client,
            url=url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            json=json,
            closure=closure,
            **kwargs,
        )

        if httpx.__version__ < "0.20.0":
            response = client.send(request, timeout=http_request_timeout)
        else:
            response = client.send(request)

        return response


class AsyncHTTPClient(BaseHTTPClient):
    async def open_async(self):
        config = self._session.config
        limits = get_http_limits(config)

        # httpx has its default Accept header and
        # server wants application/json or nothing
        self._client = httpx.AsyncClient(
            headers={"Accept": APPLICATION_JSON}, limits=limits
        )

        key = configure.keys.http_auto_retry_config
        auto_retry_config = config.get(key, None)

        if auto_retry_config:
            number_of_retries = auto_retry_config.get("number-of-retries", 3)
            retry_on_errors = auto_retry_config.get("on-errors", [])
            retry_backoff_factor = auto_retry_config.get("backoff-factor", 1)
            retry_on_methods = auto_retry_config.get("on-methods", ["GET", "POST"])

            retry_transport = RetryAsyncTransport(
                total_attempts=number_of_retries,
                on_statuses=retry_on_errors,
                on_methods=retry_on_methods,
                backoff_factor=retry_backoff_factor,
            )
            self._auto_retry_client = httpx.AsyncClient(transport=retry_transport)

    async def close_async(self):
        if self._client:
            self._client = httpx.AsyncClient(headers={"Accept": APPLICATION_JSON})
            await self._client.aclose()
            self._client = None

        if self._auto_retry_client:
            await self._auto_retry_client.aclose()
            self._auto_retry_client = None

    async def send(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        **kwargs,
    ) -> httpx.Response:
        auto_retry = kwargs.pop("auto_retry", False)
        client: httpx.AsyncClient = (
            self._auto_retry_client if auto_retry else self._client
        )

        http_request_timeout = self._filtered_timeout(kwargs=kwargs)

        request = self.build_request(
            client=client,
            url=url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            json=json,
            closure=closure,
            **kwargs,
        )
        if httpx.__version__ < "0.20.0":
            response = await client.send(request, timeout=http_request_timeout)
        else:
            response = await client.send(request)

        return response


class HTTPService(LogReporter):
    def __init__(self, session: "Session") -> None:
        super().__init__(session)
        self._session: "Session" = session

    @cached_property
    def _client(self) -> HTTPClient:
        return HTTPClient(self._session)

    @cached_property
    def _client_async(self) -> AsyncHTTPClient:
        return AsyncHTTPClient(self._session)

    @property
    def request_timeout_secs(self):
        return get_http_request_timeout_secs(self._session)

    def open(self):
        self._client.open()

    def close(self):
        self._client.close()

    def request(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        **kwargs,
    ) -> httpx.Response:
        if self._client.is_closed():
            self._client.open()

        try:
            response = self._client.send(
                url=url,
                method=method,
                headers=headers,
                data=data,
                params=params,
                json=json,
                closure=closure,
                **kwargs,
            )
        except RequestRetryException as error:
            self.error(error)
            raise error
        except (
            httpx.ConnectError,
            httpx.ConnectTimeout,
            httpx.HTTPStatusError,
            httpx.InvalidURL,
            httpx.LocalProtocolError,
            httpx.NetworkError,
            httpx.ProtocolError,
            httpx.ProxyError,
            httpx.ReadError,
            httpx.RequestError,
            httpx.ReadTimeout,
            httpx.RemoteProtocolError,
            httpx.TooManyRedirects,
            httpx.TransportError,
            httpx.TimeoutException,
        ) as error:
            self.error(
                f"An error occurred while requesting {error.request.url!r}.\n"
                f"\t{error!r}"
            )
            raise error

        self.debug(f"HTTP request response {response.status_code}: {response.text}")
        return response

    async def open_async(self):
        await self._client_async.open_async()

    async def close_async(self):
        await self._client_async.close_async()

    async def request_async(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        **kwargs,
    ) -> httpx.Response:
        if self._client_async.is_closed():
            await self._client_async.open_async()

        try:
            response = await self._client_async.send(
                url=url,
                method=method,
                headers=headers,
                data=data,
                params=params,
                json=json,
                closure=closure,
                **kwargs,
            )
        except RequestRetryException as error:
            self.error(error)
            raise error
        except (
            httpx.ConnectError,
            httpx.ConnectTimeout,
            httpx.HTTPStatusError,
            httpx.InvalidURL,
            httpx.LocalProtocolError,
            httpx.NetworkError,
            httpx.ProtocolError,
            httpx.ProxyError,
            httpx.ReadError,
            httpx.RequestError,
            httpx.ReadTimeout,
            httpx.RemoteProtocolError,
            httpx.TooManyRedirects,
            httpx.TransportError,
            httpx.TimeoutException,
        ) as error:
            self.error(
                f"An error occurred while requesting {error.request.url!r}.\n"
                f"\t{error!r}"
            )
            raise error

        self.debug(f"HTTP request response {response.status_code}: {response.text}")
        return response


def get_service(session: "Session") -> HTTPService:
    return HTTPService(session)
