import traceback
import urllib.parse
from json import JSONDecodeError
from typing import Any, Callable, Dict, Iterable, TYPE_CHECKING, Generic, TypeVar

import requests

from ._endpoint_data import EndpointData, Error, RequestMethod
from ..._configure import _RDPConfig
from ..._core.session import get_valid_session, is_open
from ..._tools import DEBUG, cached_property, get_response_reason, parse_url, urljoin
from ...content._content_type import ContentType
from ...errors import RDError

if TYPE_CHECKING:
    import pandas as pd


# --------------------------------------------------------------------------------------
#   Content data
# --------------------------------------------------------------------------------------


class Data(EndpointData):
    def __init__(
        self,
        raw: Any,
        dataframe: "pd.DataFrame" = None,
        dfbuilder: Callable[[Any, Dict[str, Any]], "pd.DataFrame"] = None,
        **kwargs,
    ):
        EndpointData.__init__(self, raw, **kwargs)
        self._dataframe = dataframe
        self._dfbuilder = dfbuilder

    @property
    def df(self):
        if self._dataframe is None and self._dfbuilder:
            self._dataframe = self._dfbuilder(self.raw, **self._kwargs)

        return self._dataframe


# --------------------------------------------------------------------------------------
#   Response object
# --------------------------------------------------------------------------------------

T = TypeVar("T")


class BaseResponse(Generic[T]):
    def __init__(self, *args, **kwargs):
        self.is_success: bool = kwargs.get("is_success")
        self.data: T = kwargs.get("content_data")
        self._status = kwargs.get("status")

        err_code = kwargs.get("error_code")
        err_message = kwargs.get("error_message")

        if err_code or err_message:
            if isinstance(err_code, list) and isinstance(err_message, list):
                errors = [Error(code, msg) for code, msg in zip(err_code, err_message)]

            else:
                errors = [Error(err_code, err_message)]

            self.errors = errors

        else:
            self.errors = []

        self._raw_response = kwargs.get("raw_response")
        self.http_response = self._raw_response

    @cached_property
    def requests_count(self):
        if isinstance(self.http_response, list):
            return len(self.http_response)
        return 1

    @property
    def request_message(self):
        if self._raw_response:
            return self._raw_response.request
        return None

    @property
    def closure(self):
        if self._raw_response:
            request = self._raw_response.request
            if isinstance(request, list):
                closure = [_request.headers.get("closure") for _request in request]
            else:
                closure = request.headers.get("closure")
            return closure
        return None

    @property
    def http_status(self):
        return self._status

    @property
    def http_headers(self):
        if self._raw_response:
            return self._raw_response.headers
        return None


class Response(BaseResponse[Data]):
    pass


# --------------------------------------------------------------------------------------
#   Response factory
# --------------------------------------------------------------------------------------


class ResponseFactory:
    def __init__(self, response_class=Response, data_class=Data):
        super().__init__()
        self.data_class = data_class
        self.response_class = response_class

    def get_raw(self, data):
        raw = data.get("content_data")
        return raw

    def get_dfbuilder(self, kwargs):
        from ...content._df_builder_factory import get_dfbuilder, DFBuildType

        content_type = kwargs.get("__content_type__", ContentType.DEFAULT)
        dfbuild_type = kwargs.get("__dfbuild_type__", DFBuildType.DATE_AS_INDEX)
        dfbuilder = get_dfbuilder(content_type, dfbuild_type)
        return dfbuilder

    def create_success(self, data, *args, **kwargs):
        inst = self.response_class(is_success=True, **data)
        raw = self.get_raw(data)
        dfbuilder = self.get_dfbuilder(kwargs)
        inst.data = self.data_class(raw, dfbuilder=dfbuilder, **kwargs)
        inst.data._owner = inst

        return inst

    def create_fail(self, data, *args, **kwargs):
        inst = self.response_class(is_success=False, **data)
        inst.data = self.data_class(data.get("content_data"))
        inst.data._owner = inst
        return inst


# --------------------------------------------------------------------------------------
#   Request factory
# --------------------------------------------------------------------------------------

request_method_value = {
    RequestMethod.POST: "POST",
    RequestMethod.PUT: "PUT",
    RequestMethod.DELETE: "DELETE",
    RequestMethod.GET: "GET",
}


class RequestFactory:
    def get_url(self, *args, **kwargs):
        url = args[1]
        return url

    def create(self, *args, **kwargs):
        session = args[0]
        url = self.get_url(*args, **kwargs)
        url_root = session._get_rdp_url_root()

        method = self.get_request_method(*args, **kwargs)
        header_parameters = self.get_header_parameters(*args, **kwargs) or {}
        path_parameters = self.get_path_parameters(*args, **kwargs)
        extended_params = kwargs.get("extended_params") or {}
        query_parameters = self.get_query_parameters(*args, **kwargs)
        query_parameters = self.extend_query_parameters(
            query_parameters, extended_params
        )
        body_parameters = self.get_body_parameters(*args, **kwargs)
        body_parameters = self.extend_body_parameters(body_parameters, extended_params)
        closure = kwargs.get("closure")

        url = self.update_url(url_root, url, path_parameters, query_parameters)

        headers = header_parameters
        if method != RequestMethod.GET:
            headers["Content-Type"] = "application/json"

        request = {
            "url": url,
            "method": request_method_value.get(method),
            "headers": headers,
            "body": body_parameters,
        }

        if closure is not None:
            request["closure"] = closure

        return request

    def update_url(self, url_root, url, path_parameters, query_parameters):
        try:
            result = parse_url(url)

            if not all([result.scheme, result.netloc, result.path]):
                if result.query and result.path:
                    url = urljoin(url_root, result.path)
                else:
                    url = urljoin(url_root, url)
            else:
                url = "".join([url_root, result.path])

            if result.query and isinstance(query_parameters, list):
                query_parameters.extend(urllib.parse.parse_qsl(result.query))

        except Exception:
            url = "/".join([url_root + "/" + url])

        if path_parameters:
            for key, value in path_parameters.items():
                value = urllib.parse.quote(value)
                url = url.replace("{" + key + "}", value)

        if self.is_multiple_query_parameters(query_parameters):
            url = self.add_multiple_query_parameters(url, query_parameters)
        elif query_parameters:
            url = self.add_query_parameters(url, query_parameters)

        return url

    def is_multiple_query_parameters(self, query_parameters: Any) -> bool:
        """Check multiple query parameters.

        Args:
            query_parameters (Any): Query parameters.

        Uses to check query parameters if they passes like
        {"universe": ["IBM.N", "ORCL.N"]} in case when query string must be constructed
        like '?universe=BNPP.PA,ORCL.N'
        """
        if isinstance(query_parameters, dict):
            return all(
                [
                    len(query_parameters) == 1,
                    isinstance(list(query_parameters.values())[0], list),
                ]
            )

        return False

    def get_request_method(self, *_, **kwargs) -> RequestMethod:
        return kwargs.get("method", RequestMethod.GET)

    def get_body_parameters(self, *_, **kwargs) -> dict:
        return kwargs.get("body_parameters") or {}

    def get_query_parameters(self, *_, **kwargs) -> list:
        return kwargs.get("query_parameters") or []

    def get_path_parameters(self, *_, **kwargs) -> dict:
        return kwargs.get("path_parameters") or {}

    def add_multiple_query_parameters(self, url, query_parameters) -> str:
        """Add multiple query parameters to query string.

        Args:
            url (str): url to construct query string.
            query_parameters (dict): query parameters to construct query string.

        Uses to construct percent-encoded query string if query parameters passed like
        {"universe": ["IBM.N", "ORCL.N"]} and must be transformed to query string like
        '?universe=BNPP.PA,ORCL.N', not like '?universe=BNPP.PA&universe=ORCL.N'

        Estimates API accepts only '?universe=BNPP.PA,ORCL.N' format to get estimates
        actual KPI measures for multiple universe.
        """
        key, v = query_parameters.popitem()
        val = ", ".join(v)
        return "?".join([url, urllib.parse.urlencode({key: val})])

    def add_query_parameters(self, url, query_parameters) -> str:
        return "?".join([url, urllib.parse.urlencode(query_parameters)])

    def extend_query_parameters(self, query_parameters, extended_params):
        return query_parameters

    def extend_body_parameters(self, body_parameters, extended_params):
        result = body_parameters
        result.update(extended_params or {})
        return result

    def get_header_parameters(self, *args, **kwargs):
        return kwargs.get("header_parameters", {})


# --------------------------------------------------------------------------------------
#   Connection object
# --------------------------------------------------------------------------------------


class HttpSessionConnection:
    def send(self, request, *args, **kwargs):
        session = args[0]

        if not is_open(session):
            raise ValueError("Session is not opened. Can't send any request")

        method = request.get("method")
        url = request.get("url")
        headers = request.get("headers")
        body = request.get("body")
        auto_retry = kwargs.get("auto_retry", False)
        session.debug(f"Send {method} request to {url}  (auto-retry={auto_retry})")
        session.debug(f"\theaders : {headers}\n\tbody : {body}")
        data = session.http_request(
            url=url,
            method=method,
            headers=headers,
            json=body,
            closure=request.get("closure"),
            auto_retry=auto_retry,
        )
        return data

    async def send_async(self, request, *args, **kwargs):
        session = args[0]

        if not is_open(session):
            raise ValueError("Session is not opened. Can't send any request")

        method = request.get("method")
        url = request.get("url")
        headers = request.get("headers")
        body = request.get("body")
        auto_retry = kwargs.get("auto_retry", False)
        session.debug(
            f"Send {method} request asynchronously to {url}  (auto-retry={auto_retry})"
        )
        session.debug(f"\theaders : {headers}\n\tbody : {body}")
        data = await session.http_request_async(
            url=url,
            method=method,
            headers=headers,
            json=body,
            closure=request.get("closure"),
            auto_retry=auto_retry,
        )
        return data


# --------------------------------------------------------------------------------------
#   Raw data parser
# --------------------------------------------------------------------------------------

success_http_codes = [
    requests.codes.ok,
    requests.codes.accepted,
    requests.codes.created,
]


class Parser:
    def process_successful_response(self, raw_response):
        status = {
            "http_status_code": raw_response.status_code,
            "http_reason": get_response_reason(raw_response),
        }

        media_type = raw_response.headers.get("content-type", "")

        if "/json" in media_type:
            try:
                content_data = raw_response.json()
                if content_data is None:
                    # Some HTTP responses, such as a DELETE,
                    # can be successful without any response body.
                    content_data = {}

                parsed_data = {
                    "status": status,
                    "raw_response": raw_response,
                    "content_data": content_data,
                }
            except (TypeError, JSONDecodeError) as error:
                message = f"Failed to process HTTP response : {str(error)}"
                status["content"] = message
                content_data = raw_response.text
                parsed_data = {
                    "status": status,
                    "raw_response": raw_response,
                    "content_data": content_data,
                }

        elif (
            "text/plain" in media_type
            or "text/html" in media_type
            or "text/xml" in media_type
            or "image/" in media_type
        ):
            content_data = raw_response.text
            parsed_data = {
                "status": status,
                "raw_response": raw_response,
                "content_data": content_data,
            }

        else:
            status["content"] = f"Unknown media type returned: {media_type}"
            parsed_data = {
                "status": status,
                "raw_response": raw_response,
            }

        return parsed_data

    def process_failed_response(self, raw_response):
        status = {
            "http_status_code": raw_response.status_code,
            "http_reason": get_response_reason(raw_response),
        }

        try:
            content_data = raw_response.json()
            content_error = content_data.get("error")

            if content_error:
                if isinstance(content_error, str):
                    content_error = {"code": None, "message": content_error}

                status["error"] = content_error
                error_code = raw_response.status_code
                error_message = content_error.get("message")
            else:
                error_code = raw_response.status_code
                error_message = raw_response.text

        except (TypeError, JSONDecodeError):
            error_code = raw_response.status_code
            error_message = raw_response.text

        if error_code == 403:
            if not error_message.endswith("."):
                error_message += ". "
            error_message += "Contact Refinitiv to check your permissions."

        parsed_data = {
            "status": status,
            "error_code": error_code,
            "error_message": error_message,
            "raw_response": raw_response,
        }

        return parsed_data

    def parse_raw_response(self, raw_response, *args, **kwargs):
        parsed_data = {}
        is_success = False

        if raw_response is None:
            return is_success, parsed_data

        is_success = raw_response.status_code in success_http_codes

        if is_success:
            parsed_data = self.process_successful_response(raw_response)

        else:
            parsed_data = self.process_failed_response(raw_response)

        return is_success, parsed_data


# --------------------------------------------------------------------------------------
#   Content data validator
# --------------------------------------------------------------------------------------


class ContentValidator:
    def validate(self, data: dict, *args, **kwargs) -> bool:
        is_valid = True
        content_data = data.get("content_data")

        if content_data is None:
            is_valid = False
            data["error_code"] = 1
            data["error_message"] = "Content data is None"

        else:
            status = content_data.get("status")
            if status == "Error":
                is_valid = False
                data["error_code"] = content_data.get("code", -1)
                data["error_message"] = content_data.get("message")

        return is_valid


class ContentTypeValidator:
    def __init__(self, allowed_content_types=None):
        if allowed_content_types is None:
            allowed_content_types = {"application/json"}
        self._allowed_content_types = allowed_content_types

    def validate(self, data: dict, *args, **kwargs) -> bool:
        # Checking only first part (type/subtype) of media_type
        # See https://httpwg.org/specs/rfc7231.html#media.type
        content_type = (
            data["raw_response"].headers.get("content-type", "").split(";")[0].strip()
        )
        is_success = content_type in self._allowed_content_types

        if not is_success:
            data["error_code"] = -1
            data["error_message"] = (
                f"Unexpected content-type in response,\n"
                f"Expected: {self._allowed_content_types}\n"
                f"Actual: {content_type}"
            )

        return is_success


# --------------------------------------------------------------------------------------
#   Data provider
# --------------------------------------------------------------------------------------


def _check_response(
    response: "Response", config: "_RDPConfig", response_class=Response
) -> None:
    if isinstance(response, response_class):
        is_raise_exception = config.get_param("raise_exception_on_error")
        if not response.is_success and is_raise_exception:
            error_code = response.errors[0].code
            error_message = response.errors[0].message
            exception_class = getattr(response, "exception_class", None)

            if exception_class:
                raise exception_class(error_code, error_message)

            else:
                raise RDError(error_code, error_message)


class ValidatorContainer:
    def __init__(
        self,
        validators: Iterable = None,
        content_validator=ContentValidator(),
        content_type_validator=ContentTypeValidator(),
        use_default_validators=True,
    ):
        self.validators = list(validators) if validators else []
        if content_validator and use_default_validators:
            self.validators.append(content_validator)
        if content_type_validator and use_default_validators:
            self.validators.append(content_type_validator)

    def validate(self, data: dict, *args, **kwargs) -> bool:
        return all(
            validator.validate(data, *args, **kwargs) for validator in self.validators
        )


class DataProvider:
    def __init__(
        self,
        connection=HttpSessionConnection(),
        request=RequestFactory(),
        response=ResponseFactory(),
        parser=Parser(),
        validator=ValidatorContainer(),
    ):
        self.connection = connection
        self.request = request
        self.response = response
        self.parser = parser
        self.validator = validator

    def _process_response(self, raw_response, *args, **kwargs):
        is_success, data = self.parser.parse_raw_response(raw_response)

        is_success = is_success and self.validator.validate(data, *args, **kwargs)

        if is_success:
            response = self.response.create_success(data, *args, **kwargs)

        else:
            response = self.response.create_fail(data, *args, **kwargs)

        return response

    def get_data(self, *args, **kwargs):
        request = self.request.create(*args, **kwargs)
        raw_response = self.connection.send(request, *args, **kwargs)
        return self._process_response(raw_response, *args, **kwargs)

    async def get_data_async(self, *args, **kwargs):
        request = self.request.create(*args, **kwargs)
        raw_response = await self.connection.send_async(request, *args, **kwargs)
        return self._process_response(raw_response, *args, **kwargs)


default_data_provider = DataProvider()


# --------------------------------------------------------------------------------------
#   Provider layer
# --------------------------------------------------------------------------------------


def emit_event(handler, *args, **kwargs):
    session = args[2]
    try:
        handler(*args, **kwargs)
    except Exception as e:
        session.error(f"{handler} callback raised exception: {e!r}")
        session.debug(traceback.format_exc())

        if DEBUG:
            raise e


class DataProviderLayer:
    def __init__(self, data_type, **kwargs):
        self._initialize(data_type, **kwargs)

    def _initialize(self, data_type, **kwargs):
        from ._data_provider_factory import make_provider

        self._kwargs = kwargs
        self._kwargs["__data_type__"] = data_type
        self._kwargs["__content_type__"] = data_type

        self._data_type = data_type
        self._content_type = data_type
        self._provider = make_provider(data_type)

    def _check_response(self, response, config):
        _check_response(response, config)

    def get_data(self, session=None, on_response=None, **kwargs):
        """
        Returns a response to the data platform

        Parameters
        ----------
        session : Session, optional
            Means default session would be used
        on_response : Callable, optional
            Callable object to process retrieved data

        Returns
        -------
        Response

        Raises
        ------
        AttributeError
            If user didn't set default session.

        """
        from ._data_provider_factory import get_url, get_api_config

        session = get_valid_session(session)
        config = session.config
        data_type = self._data_type
        url = get_url(data_type, config)
        api_config = get_api_config(data_type, config)
        auto_retry = api_config.get("auto-retry", False)
        response = self._provider.get_data(
            session, url, auto_retry=auto_retry, **kwargs, **self._kwargs
        )
        on_response and emit_event(on_response, response, self, session)
        self._check_response(response, config)
        return response

    async def get_data_async(self, session=None, on_response=None, **kwargs):
        """
        Returns a response asynchronously to the data platform

        Parameters
        ----------
        session : Session, optional
            Means default session would be used
        on_response : Callable, optional
            Callable object to process retrieved data

        Returns
        -------
        Response

        Raises
        ------
        AttributeError
            If user didn't set default session.

        """
        from ._data_provider_factory import get_url, get_api_config

        session = get_valid_session(session)
        config = session.config
        data_type = self._data_type
        url = get_url(data_type, config)
        api_config = get_api_config(data_type, config)
        auto_retry = api_config.get("auto-retry", False)
        response = await self._provider.get_data_async(
            session, url, auto_retry=auto_retry, **kwargs, **self._kwargs
        )
        on_response and emit_event(on_response, response, self, session)
        return response

    def __repr__(self):
        s = super().__repr__()
        s = s.replace(">", f" {{name='{self._kwargs.get('universe')}'}}>")
        return s
