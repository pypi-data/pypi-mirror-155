import re
from json import JSONDecodeError
from typing import Tuple, List

import pandas as pd
import requests

from .._content_provider import (
    HistoricalDataProvider,
    field_timestamp_by_day_interval_type,
    axis_by_day_interval_type,
)
from .._content_type import ContentType
from .._intervals import DayIntervalType, get_day_interval_type, Intervals
from .._join_responses import join_historical_responses
from ..._errors import RDError
from ..._tools import (
    get_response_reason,
    make_enum_arg_parser,
    custom_insts_datetime_adapter,
)
from ..._tools._dataframe import convert_df_columns_to_datetime
from ...delivery._data._data_provider import (
    RequestFactory,
    ResponseFactory,
    Parser,
    success_http_codes,
    ContentValidator,
    DataProvider,
    DataProviderLayer,
    ContentTypeValidator,
    ValidatorContainer,
    Response,
)
from ...delivery._data._endpoint_data import RequestMethod

content_type_by_day_interval_type = {
    DayIntervalType.INTER: ContentType.CUSTOM_INSTRUMENTS_INTERDAY_SUMMARIES,
    DayIntervalType.INTRA: ContentType.CUSTOM_INSTRUMENTS_INTRADAY_SUMMARIES,
}

# a20140be-3648-4892-9d1b-ce78ee8617fd
is_instrument_id = re.compile("[a-z0-9]{8}(-[a-z0-9]{4}){3}-[a-z0-9]{12}")


def get_query_params_from_kwargs(kwargs: dict, params: dict) -> list:
    query_params = []
    for param_name, request_param_name in params.items():
        value = kwargs.get(param_name)
        if value:
            query_params.append((request_param_name, value))
    return query_params


def get_params(params_details, data):
    retval = []
    for value in params_details:
        param_name = value.get("param_name")
        request_param_name = value.get("request_param_name")
        convert_function = value.get("convert_function")
        param = data.get(param_name)
        if not param:
            continue

        if convert_function:
            param = convert_function(param)
        retval.append((request_param_name, param))
    return retval


def get_content_type_by_interval(interval) -> ContentType:
    day_interval_type = get_day_interval_type(interval)
    return content_type_by_day_interval_type.get(day_interval_type)


# --------------------------------------------------------------------------------------
#   Response factory
# --------------------------------------------------------------------------------------


def custom_instruments_build_df(content_data: dict, **kwargs) -> pd.DataFrame:
    if isinstance(content_data, dict):
        content_data = [content_data]
    dataframe = pd.DataFrame(content_data)
    dataframe.fillna(pd.NA, inplace=True)
    return dataframe


def custom_instruments_intervals_build_df(content_data: dict, **kwargs) -> pd.DataFrame:
    data = content_data.get("data")
    headers = content_data.get("headers", [])
    columns = [header.get("name") for header in headers]
    dataframe = pd.DataFrame(data, columns=columns)
    convert_df_columns_to_datetime(dataframe, pattern="DATE", utc=True, delete_tz=True)
    dataframe.fillna(pd.NA, inplace=True)
    return dataframe


# --------------------------------------------------------------------------------------
#   Request factory
# --------------------------------------------------------------------------------------


def get_user_id(session=None) -> str:
    provider = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        universe="S)IntrumentT.UUID",
    )
    provider._check_response = lambda *args, **kwargs: None
    response = provider.get_data(session=session)
    errors = response.errors
    messages = [error.message for error in errors]
    for message in messages:
        if message.startswith(
            "Validation Error: .UUID suffix UUID not matched with userID"
        ):
            _, user_id = message.rsplit(" ", 1)
            return user_id


def get_correct_symbol(symbol, session):
    # "MyNewInstrument"
    retval = symbol
    if not retval.startswith("S)"):
        retval = f"S){retval}"
    # "S)MyNewInstrument"
    if "." not in retval:
        user_id = get_user_id(session)
        retval = f"{retval}.{user_id}"
    # "S)MyNewInstrument.GE-1234"
    return retval


def convert_json_to_pandas(data: dict) -> pd.DataFrame:
    content_data = data.get("content_data")
    if isinstance(content_data, dict):
        content_data = [content_data]
    dataframe = pd.DataFrame(content_data)
    dataframe.fillna(pd.NA, inplace=True)
    return dataframe


def convert_historical_json_to_pandas(data: dict) -> pd.DataFrame:
    content_data = data.get("content_data", {})
    _data = content_data.get("data")
    headers = content_data.get("headers", [])
    columns = [header.get("name") for header in headers]
    dataframe = pd.DataFrame(_data, columns=columns)
    dataframe.fillna(pd.NA, inplace=True)
    return dataframe


class BaseRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        if self.get_request_method(*args, **kwargs) == RequestMethod.POST:
            return super().get_url(*args, **kwargs)
        return super().get_url(*args, **kwargs) + "/{universe}"

    def get_path_parameters(self, *args, **kwargs):
        if self.get_request_method(*args, **kwargs) == RequestMethod.POST:
            return {}
        session = args[0]
        universe = kwargs.get("universe")
        if universe is None:
            raise RDError(-1, "universe can't be None")

        if not is_instrument_id.match(universe):
            universe = get_correct_symbol(universe, session)
        return {"universe": universe}


class CustomInstsRequestFactory(BaseRequestFactory):
    def get_body_parameters(self, *args, **kwargs):
        body_parameters = {}
        if self.get_request_method(*args, **kwargs) not in [
            RequestMethod.POST,
            RequestMethod.PUT,
        ]:
            return body_parameters

        symbol = kwargs.get("symbol")
        if symbol:
            if not symbol.startswith("S)"):
                symbol = f"S){symbol}"
            if "." not in symbol:
                session = args[0]
                user_id = get_user_id(session)
                symbol = f"{symbol}.{user_id}"
            body_parameters["symbol"] = symbol

        currency = kwargs.get("currency")
        if currency:
            body_parameters["currency"] = currency

        description = kwargs.get("description")
        if description:
            body_parameters["description"] = description

        exchange_name = kwargs.get("exchange_name")
        if exchange_name:
            body_parameters["exchangeName"] = exchange_name

        formula = kwargs.get("formula")
        if formula:
            body_parameters["formula"] = formula

        holidays = kwargs.get("holidays")
        if holidays:
            body_parameters["holidays"] = holidays

        instrument_name = kwargs.get("instrument_name")
        if instrument_name:
            body_parameters["instrumentName"] = instrument_name

        time_zone = kwargs.get("time_zone")
        if time_zone:
            body_parameters["timeZone"] = time_zone

        return body_parameters


# --------------------------------------------------------------------------------------
#   Raw data parser
# --------------------------------------------------------------------------------------


class CustomInstsParser(Parser):
    def parse_raw_response(self, raw_response, *args, **kwargs):
        parsed_data = {}
        is_success = False

        if raw_response is None:
            return is_success, parsed_data

        is_success = raw_response.status_code in success_http_codes + [
            requests.codes.no_content
        ]

        if is_success:
            parsed_data = self.process_successful_response(raw_response)

        else:
            parsed_data = self.process_failed_response(raw_response)

        return is_success, parsed_data

    def process_failed_response(self, raw_response):
        status = {
            "http_status_code": raw_response.status_code,
            "http_reason": get_response_reason(raw_response),
        }

        try:
            content_data = raw_response.json()
            content_error = content_data.get("error")

            if content_error:
                status["error"] = content_error
                error_code = content_error.get("code")
                if isinstance(error_code, str) and not error_code.isdigit():
                    error_code = raw_response.status_code
                error_message = content_error.get("message")
                errors = content_error.get("errors", {})
                errors = [error.get("reason") for error in errors if error]
                if errors:
                    errors = "\n".join(errors)
                    error_message = f"{error_message}: {errors}"
            elif "state" in content_data:
                state = content_data.get("state", {})
                error_code = state.get("code")
                data = content_data.get("data", [])
                reasons = [_data.get("reason", "") for _data in data]
                reason = "\n".join(reasons)
                error_message = f"{state.get('message')}: {reason}"
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


# --------------------------------------------------------------------------------------
#   Content data validator
# --------------------------------------------------------------------------------------


class CustomInstsContentValidator(ContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = True
        content_data = data.get("content_data")
        status = data.get("status")
        status_code = status.get("http_status_code")

        if content_data is None and status_code != 204:
            is_valid = False
            data["error_code"] = 1
            data["error_message"] = "Content data is None"

        return is_valid


# --------------------------------------------------------------------------------------
#   Request factory
# --------------------------------------------------------------------------------------

interval_arg_parser = make_enum_arg_parser(Intervals, can_be_lower=True)


class CustomInstsSearchRequestFactory(RequestFactory):
    def get_query_parameters(self, *args, **kwargs):
        access = kwargs.get("access")
        return [
            ("access", access),
        ]


class CustomInstsEventsRequestFactory(BaseRequestFactory):
    def get_query_parameters(self, *args, **kwargs):
        query_params = get_params(
            [
                {
                    "param_name": "start",
                    "request_param_name": "start",
                    "convert_function": custom_insts_datetime_adapter.get_str,
                },
                {
                    "param_name": "end",
                    "request_param_name": "end",
                    "convert_function": custom_insts_datetime_adapter.get_str,
                },
                {"param_name": "count", "request_param_name": "count"},
            ],
            kwargs,
        )
        return query_params


class CustomInstsSummariesRequestFactory(BaseRequestFactory):
    def get_field_timestamp(self, *args, day_interval_type=None, **kwargs):
        return field_timestamp_by_day_interval_type.get(day_interval_type)

    def get_query_parameters(self, *args, **kwargs):
        query_params = get_params(
            [
                {
                    "param_name": "start",
                    "request_param_name": "start",
                    "convert_function": custom_insts_datetime_adapter.get_str,
                },
                {
                    "param_name": "end",
                    "request_param_name": "end",
                    "convert_function": custom_insts_datetime_adapter.get_str,
                },
                {"param_name": "count", "request_param_name": "count"},
            ],
            kwargs,
        )
        interval = kwargs.get("interval")
        if interval:
            interval = interval_arg_parser.get_str(interval)
            query_params.append(("interval", interval))
        return query_params


# --------------------------------------------------------------------------------------
#   Data provider
# --------------------------------------------------------------------------------------


class CustomInstsEventsDataProvider(HistoricalDataProvider):
    @staticmethod
    def _join_responses(
        responses: List[Tuple[str, "Response"]],
        fields: List[str],
        kwargs,
    ) -> "Response":
        axis_name = "Timestamp"
        return join_historical_responses(responses, axis_name, fields)


class CustomInstsSummariesDataProvider(HistoricalDataProvider):
    @staticmethod
    def _join_responses(
        responses: List[Tuple[str, "Response"]],
        fields: List[str],
        kwargs,
    ) -> "Response":
        axis_name = axis_by_day_interval_type.get(kwargs.get("day_interval_type"))
        return join_historical_responses(responses, axis_name, fields)


custom_instrument_data_provider = DataProvider(
    response=ResponseFactory(),
    request=CustomInstsRequestFactory(),
    parser=CustomInstsParser(),
    validator=ValidatorContainer(
        content_validator=CustomInstsContentValidator(),
        content_type_validator=ContentTypeValidator({"application/json", ""}),
    ),
)
custom_instrument_search_data_provider = DataProvider(
    request=CustomInstsSearchRequestFactory(),
    parser=CustomInstsParser(),
    validator=ValidatorContainer(
        content_validator=CustomInstsContentValidator(),
        content_type_validator=ContentTypeValidator({"application/json", ""}),
    ),
)

custom_instruments_events_data_provider = CustomInstsEventsDataProvider(
    request=CustomInstsEventsRequestFactory(),
)
custom_instruments_intraday_summaries_data_provider = CustomInstsSummariesDataProvider(
    request=CustomInstsSummariesRequestFactory(),
)
custom_instruments_interday_summaries_data_provider = CustomInstsSummariesDataProvider(
    request=CustomInstsSummariesRequestFactory(),
)
