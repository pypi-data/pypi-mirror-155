import asyncio
from abc import abstractmethod
from typing import Tuple, List

from ._intervals import DayIntervalType
from ._join_responses import get_first_success_response
from .._errors import RDError
from ..delivery._data import _data_provider
from ..delivery._data._data_provider import DataProvider, Response


# ---------------------------------------------------------------------------
#   Raw data parser
# ---------------------------------------------------------------------------


class ErrorParser(_data_provider.Parser):
    def process_failed_response(self, raw_response):
        parsed_data = super().process_failed_response(raw_response)
        status = parsed_data.get("status", {})
        error = status.get("error", {})
        errors = error.get("errors", [])
        error_code = parsed_data.get("error_code")
        error_message = parsed_data.get("error_message", "")
        err_msgs = []
        err_codes = []
        for err in errors:
            reason = err.get("reason")
            if reason:
                err_codes.append(error_code)
                err_msgs.append(f"{error_message}: {reason}")

        if err_msgs and err_codes:
            parsed_data["error_code"] = err_codes
            parsed_data["error_message"] = err_msgs

        return parsed_data


# ---------------------------------------------------------------------------
#   Content data validator
# ---------------------------------------------------------------------------


def get_invalid_universes(universes):
    result = []
    for universe in universes:
        if universe.get("Organization PermID") == "Failed to resolve identifier(s).":
            result.append(universe.get("Instrument"))
    return result


def get_universe_from_raw_response(raw_response):
    universe = raw_response.url.params["universe"]
    universe = universe.split(",")
    return universe


class UniverseContentValidator(_data_provider.ContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = super().validate(data)
        if not is_valid:
            return is_valid

        content_data = data.get("content_data", {})
        error = content_data.get("error", {})
        universes = content_data.get("universe", [])
        invalid_universes = get_invalid_universes(universes)

        if error:
            is_valid = False
            data["error_code"] = error.get("code")

            error_message = error.get("description")
            if error_message == "Unable to resolve all requested identifiers.":
                universe = get_universe_from_raw_response(data["raw_response"])
                error_message = f"{error_message} Requested items: {universe}"

            if not error_message:
                error_message = error.get("message")
                errors = error.get("errors")
                if isinstance(errors, list):
                    errors = "\n".join(map(str, errors))
                    error_message = f"{error_message}:\n{errors}"
            data["error_message"] = error_message

        elif invalid_universes:
            data["error_message"] = f"Failed to resolve identifiers {invalid_universes}"

        return is_valid


# ---------------------------------------------------------------------------
#   Provider layer
# ---------------------------------------------------------------------------


class ContentProviderLayer(_data_provider.DataProviderLayer):
    def __init__(self, content_type, **kwargs):
        _data_provider.DataProviderLayer.__init__(
            self,
            data_type=content_type,
            **kwargs,
        )


# ---------------------------------------------------------------------------
#   DataProvider
# ---------------------------------------------------------------------------


class HistoricalDataProvider(DataProvider):
    @staticmethod
    @abstractmethod
    def _join_responses(
        responses: List[Tuple[str, Response]],
        fields: List[str],
        kwargs,
    ):
        pass

    async def _create_task(self, name, *args, **kwargs) -> Tuple[str, Response]:
        kwargs["universe"] = name
        response = await super().get_data_async(*args, **kwargs)
        return name, response

    def get_data(self, *args, **kwargs) -> Response:
        universe = kwargs.get("universe", [])
        fields = copy_fields(kwargs.get("fields"))
        responses = []
        for inst_name in universe:
            kwargs["universe"] = inst_name
            response = super().get_data(*args, **kwargs)
            responses.append((inst_name, response))

        validate_responses(responses)
        return self._join_responses(responses, fields, kwargs)

    async def get_data_async(self, *args, **kwargs) -> Response:
        universe = kwargs.get("universe", [])
        fields = copy_fields(kwargs.get("fields"))
        tasks = []
        for inst_name in universe:
            tasks.append(self._create_task(inst_name, *args, **kwargs))

        responses = await asyncio.gather(*tasks)
        return self._join_responses(responses, fields, kwargs)


def copy_fields(fields: List[str]) -> List[str]:
    if fields is None:
        return []

    if not isinstance(fields, list):
        raise AttributeError(f"fields not support type {type(fields)}")

    return fields[:]


def validate_responses(responses: List[Tuple[str, Response]]):
    response = get_first_success_response(responses)
    if response is None:
        error_message = "ERROR: No successful response.\n"
        for inst_name, response in responses:
            if response.errors:
                error = response.errors[0]
                error_message += "({}, {}), ".format(error.code, error.message)
        error_message = error_message[:-2]
        raise RDError(1, f"No data to return, please check errors: {error_message}")


field_timestamp_by_day_interval_type = {
    DayIntervalType.INTER: "DATE",
    DayIntervalType.INTRA: "DATE_TIME",
}
axis_by_day_interval_type = {
    DayIntervalType.INTRA: "Timestamp",
    DayIntervalType.INTER: "Date",
}
