from ._enums import StatTypes, Frequency, SortOrder
from .._content_provider import UniverseContentValidator, ErrorParser
from .._join_responses import join_responses
from ..._tools import ArgsParser
from ..._tools import universe_arg_parser, make_enum_arg_parser
from ..._tools._datetime import ownership_datetime_adapter
from ...delivery._data._data_provider import (
    DataProvider,
    RequestFactory,
    ValidatorContainer,
)

MAX_LIMIT = 100


def get_correct_data_for_df(content_data):
    if not isinstance(content_data, list):
        return content_data

    if not content_data:
        return dict()

    _data = []
    for i in content_data:
        _data.extend(i["data"])

    headers = content_data[0].get("headers")
    if headers and isinstance(headers[0], list):
        headers = headers[0]

    result = {"data": _data, "headers": headers}
    return result


def parse_str(param):
    if isinstance(param, str):
        return param
    raise ValueError(f"Invalid type, expected str: {type(param)} is given")


class OwnershipRequestFactory(RequestFactory):
    def get_query_parameters(self, *_, **kwargs) -> list:
        query_parameters = []
        universe = kwargs.get("universe")
        if isinstance(universe, list):
            universe = list(set(universe))
        universe = universe_arg_parser.get_str(universe, delim=",")
        query_parameters.append(("universe", universe))

        stat_type = kwargs.get("stat_type")
        if stat_type is not None:
            stat_type = stat_types_ownership_arg_parser.get_str(stat_type)
            query_parameters.append(("statType", stat_type))

        offset = kwargs.get("offset")
        if offset is not None:
            query_parameters.append(("offset", offset))

        limit = kwargs.get("limit")
        if limit is not None:
            query_parameters.append(("limit", limit))

        sort_order = kwargs.get("sort_order")
        if sort_order is not None:
            sort_order = sort_order_ownership_arg_parser.get_str(sort_order)
            query_parameters.append(("sortOrder", sort_order))

        frequency = kwargs.get("frequency")
        if frequency is not None:
            frequency = frequency_ownership_arg_parser.get_str(frequency)
            query_parameters.append(("frequency", frequency))

        start = kwargs.get("start")
        if start is not None:
            start = ownership_datetime_adapter.get_str(start)
            query_parameters.append(("start", start))

        end = kwargs.get("end")
        if end is not None:
            end = ownership_datetime_adapter.get_str(end)
            query_parameters.append(("end", end))

        count = kwargs.get("count")
        if count is not None:
            query_parameters.append(("count", count))

        return query_parameters

    def extend_query_parameters(self, query_parameters, extended_params):
        # query_parameters -> [("param1", "val1"), ]
        result = dict(query_parameters)
        # result -> {"param1": "val1"}
        result.update(extended_params)
        # result -> {"param1": "val1", "extended_param": "value"}
        # return [("param1", "val1"), ("extended_param", "value")]
        return list(result.items())


class OwnershipDataProvider(DataProvider):
    def get_data(self, *args, **kwargs):
        limit = kwargs.get("limit")

        if limit is None:
            response = super().get_data(*args, **kwargs)

        else:
            responses = []

            for offset in range(0, limit, MAX_LIMIT):
                _kwargs = kwargs
                _kwargs["limit"] = (
                    MAX_LIMIT if offset < limit - MAX_LIMIT else limit - offset
                )
                _kwargs["offset"] = offset if offset else None
                response = super().get_data(*args, **kwargs)
                responses.append(response)

            response = join_responses(responses, reset_index=True)

        return response

    async def get_data_async(self, *args, **kwargs):
        limit = kwargs.get("limit")

        if limit is None:
            response = await super().get_data_async(*args, **kwargs)

        else:
            responses = []

            for offset in range(0, limit, MAX_LIMIT):
                _kwargs = kwargs
                _kwargs["limit"] = (
                    MAX_LIMIT if offset < limit - MAX_LIMIT else limit - offset
                )
                _kwargs["offset"] = offset if offset else None
                response = await super().get_data_async(*args, **kwargs)
                responses.append(response)

            response = join_responses(responses, reset_index=True)

        return response


universe_ownership_arg_parser = ArgsParser(parse_str)
stat_types_ownership_arg_parser = make_enum_arg_parser(StatTypes)
sort_order_ownership_arg_parser = make_enum_arg_parser(SortOrder)
frequency_ownership_arg_parser = make_enum_arg_parser(Frequency)

ownership_data_provider = OwnershipDataProvider(
    request=OwnershipRequestFactory(),
    validator=ValidatorContainer(content_validator=UniverseContentValidator()),
    parser=ErrorParser(),
)
