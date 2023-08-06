# coding: utf8
import copy
import re
from enum import Enum, unique
from typing import Union, List, Tuple, TYPE_CHECKING

from .._content_provider import HistoricalDataProvider
from .._content_type import ContentType
from .._intervals import (
    DayIntervalType,
    Intervals,
    interval_arg_parser,
    get_day_interval_type,
)
from .._join_responses import join_historical_responses
from ..._tools import (
    urljoin,
    fields_arg_parser,
    make_enum_arg_parser,
)
from ..._tools._datetime import hp_datetime_adapter
from ...delivery._data._data_provider import (
    ResponseFactory,
    ContentValidator,
    RequestFactory,
)

if TYPE_CHECKING:
    from ...delivery._data._data_provider import Response

user_has_no_permissions_expr = re.compile(
    r"TS\.((Interday)|(Intraday))\.UserNotPermission\.[0-9]{5}"
)


# --------------------------------------------------------------------------------------
#   EventTypes
# --------------------------------------------------------------------------------------


@unique
class EventTypes(Enum):
    """
    The list of market events (comma delimiter), supported event types are trade,
    quote and correction.
    Note: Currently support only single event type.
        If request with multiple event types,
        the backend will pick up the first event type to proceed.
    """

    TRADE = "trade"
    QUOTE = "quote"
    CORRECTION = "correction"


event_types_arg_parser = make_enum_arg_parser(EventTypes)

# --------------------------------------------------------------------------------------
#   Intervals
# --------------------------------------------------------------------------------------


axis_by_day_interval_type = {
    DayIntervalType.INTRA: "Timestamp",
    DayIntervalType.INTER: "Date",
}

content_type_by_day_interval_type = {
    DayIntervalType.INTER: ContentType.HISTORICAL_PRICING_INTERDAY_SUMMARIES,
    DayIntervalType.INTRA: ContentType.HISTORICAL_PRICING_INTRADAY_SUMMARIES,
}


def get_content_type_by_interval(
    interval: Union[str, Intervals, DayIntervalType]
) -> ContentType:
    day_interval_type = get_day_interval_type(interval)
    return content_type_by_day_interval_type.get(day_interval_type)


# --------------------------------------------------------------------------------------
#   Adjustments
# --------------------------------------------------------------------------------------


@unique
class Adjustments(Enum):
    """
    The list of adjustment types (comma delimiter) that tells the system whether
     to apply or not apply CORAX (Corporate Actions) events or
     exchange/manual corrections to historical time series data.

     The supported values of adjustments :

        UNADJUSTED - Not apply both exchange/manual corrections and CORAX
        EXCHANGE_CORRECTION - Apply exchange correction adjustment to historical pricing
        MANUAL_CORRECTION - Apply manual correction adjustment to historical pricing
                            i.e. annotations made by content analysts
        CCH - Apply Capital Change adjustment to historical Pricing due
              to Corporate Actions e.g. stock split
        CRE - Apply Currency Redenomination adjustment
              when there is redenomination of currency
        RPO - Apply Reuters Price Only adjustment
              to adjust historical price only not volume
        RTS - Apply Reuters TimeSeries adjustment
              to adjust both historical price and volume
        QUALIFIERS - Apply price or volume adjustment
              to historical pricing according to trade/quote qualifier
              summarization actions
    """

    UNADJUSTED = "unadjusted"
    EXCHANGE_CORRECTION = "exchangeCorrection"
    MANUAL_CORRECTION = "manualCorrection"
    CCH = "CCH"
    CRE = "CRE"
    RPO = "RPO"
    RTS = "RTS"
    QUALIFIERS = "qualifiers"


adjustments_arg_parser = make_enum_arg_parser(Adjustments)


# --------------------------------------------------------------------------------------
#   MarketSession
# --------------------------------------------------------------------------------------


@unique
class MarketSession(Enum):
    """
    The marketsession parameter represents a list of interested official durations
        in which trade and quote activities occur for a particular universe.

    The supported values of marketsession :

        PRE - specifies that data returned
              should include data during pre-market session
        NORMAL - specifies that data returned
                 should include data during normal market session
        POST - specifies that data returned
               should include data during post-market session
    """

    PRE = "pre"
    NORMAL = "normal"
    POST = "post"


market_sessions_arg_parser = make_enum_arg_parser(MarketSession)


# --------------------------------------------------------------------------------------
#   ContentValidator
# --------------------------------------------------------------------------------------


class HistoricalPricingContentValidator(ContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = True
        content_data = data.get("content_data")

        if not content_data:
            is_valid = False

        elif isinstance(content_data, list) and len(content_data):
            content_data = content_data[0]
            status = content_data.get("status", {})
            code = status.get("code", "")

            if status and user_has_no_permissions_expr.match(code):
                is_valid = False
                data["status"]["error"] = status
                data["errors"] = [(code, status.get("message"))]

            elif "Error" in code:
                is_valid = False
                data["status"]["error"] = status
                data["errors"] = [(code, status.get("message"))]

                if not (content_data.keys() - {"universe", "status"}):
                    is_valid = False

                elif "UserRequestError" in code:
                    is_valid = True

            elif not content_data.get("data"):
                is_valid = False

        return is_valid


# --------------------------------------------------------------------------------------
#   Response
# --------------------------------------------------------------------------------------


response_errors = {
    "default": "{error_message}. Requested ric: {rics}. Requested fields: {fields}",
    "TS.Intraday.UserRequestError.90001": "{rics} - The universe is not found",
    "TS.Intraday.Warning.95004": "{rics} - Trades interleaving with corrections is "
    "currently not supported. Corrections will not be returned.",
    "TS.Intraday.UserRequestError.90006": "{error_message} Requested ric: {rics}",
}


class HistoricalPricingResponseFactory(ResponseFactory):
    def get_raw(self, data):
        raw = data.get("content_data", [{}])
        raw = raw[0]
        return raw

    def create_success(self, data, *args, **kwargs):
        raw = self.get_raw(data)
        error_code = data.get("status_code") or (
            raw.get("status").get("code") if raw.get("status") else None
        )
        if error_code:
            self._compile_error_message(error_code, data, **kwargs)
        return super().create_success(data, *args, **kwargs)

    def create_fail(self, data, *args, **kwargs):
        raw = self.get_raw(data)
        status = raw.get("status", {})
        error_code = data.get("error_code", status.get("code"))
        self._compile_error_message(error_code, data, **kwargs)
        return super().create_fail(data, *args, **kwargs)

    @staticmethod
    def _compile_error_message(error_code: str, data: dict, **kwargs):
        """Compile error message in human readable format."""
        content_data = data.get("content_data")[0] if data.get("content_data") else {}
        error_message = data.get("error_message") or content_data.get("status", {}).get(
            "message"
        )
        fields = kwargs.get("fields")
        rics = (
            content_data.get("universe").get("ric")
            if content_data
            else kwargs.get("universe")
        )

        if error_code not in response_errors.keys():
            # Need to add error_code to data because different structure of responses
            data["error_code"] = error_code
            data["error_message"] = response_errors["default"].format(
                error_message=error_message, rics=rics, fields=fields
            )
        else:
            data["error_code"] = error_code
            data["error_message"] = response_errors[error_code].format(
                rics=rics, error_message=error_message
            )


# --------------------------------------------------------------------------------------
#   Request
# --------------------------------------------------------------------------------------


class HistoricalPricingRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        url = args[1]
        url = urljoin(url, "/{universe}")
        return url

    def get_path_parameters(self, *_, **kwargs):
        universe = kwargs.get("universe")
        if universe is None:
            return {}
        return {"universe": universe}

    def get_field_timestamp(self, *args, **kwargs):
        return "DATE_TIME"

    def get_query_parameters(self, *args, **kwargs):
        query_parameters = []

        #
        # start
        #
        start = kwargs.get("start")
        if start:
            start = hp_datetime_adapter.get_str(start)
            query_parameters.append(("start", start))

        #
        # end
        #
        end = kwargs.get("end")
        if end:
            end = hp_datetime_adapter.get_str(end)
            query_parameters.append(("end", end))

        #
        # adjustments
        #
        adjustments = kwargs.get("adjustments")
        if adjustments:
            adjustments = adjustments_arg_parser.get_str(adjustments, delim=",")
            query_parameters.append(("adjustments", adjustments))

        #
        # market_sessions
        #
        market_sessions = kwargs.get("sessions")
        if market_sessions:
            market_sessions = market_sessions_arg_parser.get_str(
                market_sessions, delim=","
            )
            query_parameters.append(("sessions", market_sessions))

        #
        # count
        #
        count = kwargs.get("count") or 1
        if count < 1:
            raise AttributeError("Count minimum value is 1")

        if count > 1:
            query_parameters.append(("count", count))

        #
        # fields
        #
        fields = copy_fields(kwargs.get("fields"))
        if fields:
            fields = fields_arg_parser.get_list(fields)
            field_timestamp = self.get_field_timestamp(*args, **kwargs)
            if field_timestamp not in fields:
                fields.append(field_timestamp)
            query_parameters.append(("fields", ",".join(fields)))

        return query_parameters


class HistoricalPricingEventsRequestFactory(HistoricalPricingRequestFactory):
    def get_query_parameters(self, *args, **kwargs):
        query_parameters = super().get_query_parameters(*args, **kwargs)

        #
        # event_types
        #
        event_types = kwargs.get("event_types")
        if event_types:
            event_types = event_types_arg_parser.get_str(event_types, delim=",")
            query_parameters.append(("eventTypes", event_types))

        return query_parameters


field_timestamp_by_day_interval_type = {
    DayIntervalType.INTER: "DATE",
    DayIntervalType.INTRA: "DATE_TIME",
}


class HistoricalPricingSummariesRequestFactory(HistoricalPricingRequestFactory):
    def get_field_timestamp(self, *args, day_interval_type=None, **kwargs):
        return field_timestamp_by_day_interval_type.get(day_interval_type)

    def get_query_parameters(self, *args, **kwargs):
        query_parameters = super().get_query_parameters(*args, **kwargs)

        #
        # interval
        #
        interval = kwargs.get("interval")
        if interval:
            interval = interval_arg_parser.get_str(interval)
            query_parameters.append(("interval", interval))

        return query_parameters


# --------------------------------------------------------------------------------------
#   Providers
# --------------------------------------------------------------------------------------


class HPEventsDataProvider(HistoricalDataProvider):
    @staticmethod
    def _join_responses(
        responses: List[Tuple[str, "Response"]],
        fields: List[str],
        kwargs,
    ) -> "Response":
        axis_name = "Timestamp"
        return join_historical_responses(responses, axis_name, fields)


class HPSummariesDataProvider(HistoricalDataProvider):
    @staticmethod
    def _join_responses(
        responses: List[Tuple[str, "Response"]],
        fields: List[str],
        kwargs,
    ) -> "Response":
        axis_name = axis_by_day_interval_type.get(kwargs.get("day_interval_type"))
        return join_historical_responses(responses, axis_name, fields)


hp_events_data_provider = HPEventsDataProvider(
    request=HistoricalPricingEventsRequestFactory(),
    response=HistoricalPricingResponseFactory(),
    validator=HistoricalPricingContentValidator(),
)

hp_summaries_data_provider = HPSummariesDataProvider(
    request=HistoricalPricingSummariesRequestFactory(),
    response=HistoricalPricingResponseFactory(),
    validator=HistoricalPricingContentValidator(),
)


def copy_fields(fields: List[str]) -> List[str]:
    if fields is None:
        return []

    if not isinstance(fields, list):
        raise AttributeError(f"fields not support type {type(fields)}")

    return fields[:]
