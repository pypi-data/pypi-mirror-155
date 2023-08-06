# coding: utf8

import numpy
from pandas import DataFrame
from pandas import to_numeric

from ..._tools._common import universe_arg_parser, fields_arg_parser
from ...content._content_provider import ErrorParser
from ...delivery._data._data_provider import (
    DataProvider,
    RequestFactory,
    ResponseFactory,
    ContentValidator,
    ValidatorContainer,
)
from ...delivery._stream.stream_cache import StreamCache


# ---------------------------------------------------------------------------
#   Response factory
# ---------------------------------------------------------------------------


class PriceCache:
    def __init__(self, cache: dict):
        self._cache = cache

    def keys(self):
        return self._cache.keys()

    def values(self):
        return self._cache.values()

    def items(self):
        return self._cache.items()

    def __iter__(self):
        return PricingCacheIterator(self)

    def __getitem__(self, name):
        if name in self.keys():
            return self._cache[name]
        raise KeyError(f"{name} not in PriceCache")

    def __len__(self):
        return len(self.keys())

    def __str__(self):
        return str(self._cache)


class PricingCacheIterator:
    def __init__(self, price_cache: PriceCache):
        self._price_cache = price_cache
        self._universe = list(price_cache.keys())
        self._index = 0

    def __next__(self):
        if self._index < len(self._universe):
            name = self._universe[self._index]
            result = self._price_cache[name]
            self._index += 1
            return result
        raise StopIteration()


def create_price_cache(data: dict, fields) -> PriceCache:
    cache = {}
    for item in data:
        key = item.get("Key")
        if key:
            name = key.get("Name")
            service = key.get("Service")
            status = item.get("State")
            cache[name] = StreamCache(
                name=name,
                fields=fields,
                service=service,
                status=status,
                record=item,
            )
    return PriceCache(cache)


def _get_field_value(item_fields, field):
    if item_fields.get(field) is None:
        return numpy.nan
    else:
        return item_fields.get(field)


def _get_field_values(fields, item):
    if item["Type"] == "Status":
        status = numpy.nan
        _code = item["State"]["Code"]
        if _code == "NotEntitled":
            status = "#N/P"
        elif _code == "NotFound":
            status = "#N/F"
        return numpy.full(len(fields), status)
    else:
        return numpy.array([_get_field_value(item["Fields"], f) for f in fields])


def _convert_pricing_json_to_pandas(data, universe, fields):
    data = numpy.array([_get_field_values(fields, item) for item in data])
    df = DataFrame(data, columns=fields, index=universe)
    df = df.apply(to_numeric, errors="ignore")
    if not df.empty:
        df = df.convert_dtypes()
    df = df.reset_index()
    df = df.rename(columns={"index": "Instruments"})
    return df


def pricing_build_df(raw, universe, fields, **kwargs):
    if not fields:
        fields = set()
        for item in raw:
            fields |= item.get("Fields", {}).keys()

        fields = tuple(fields)

    df = _convert_pricing_json_to_pandas(raw, universe, fields)
    return df


class PricingResponseFactory(ResponseFactory):
    def create_success(self, data, *args, **kwargs):
        inst = super().create_success(data, *args, **kwargs)
        content_data = data.get("content_data")
        fields = kwargs.get("fields")
        inst.data.prices = create_price_cache(content_data, fields)
        return inst


# ---------------------------------------------------------------------------
#   Request factory
# ---------------------------------------------------------------------------


class PricingRequestFactory(RequestFactory):
    def get_query_parameters(self, *args, **kwargs) -> list:
        query_parameters = []

        #
        # universe
        #
        universe = kwargs.get("universe")
        if universe:
            universe = universe_arg_parser.get_str(universe, delim=",")
            query_parameters.append(("universe", universe))

        #
        # fields
        #
        fields = kwargs.get("fields")
        if fields:
            fields = fields_arg_parser.get_str(fields, delim=",")
            query_parameters.append(("fields", fields))

        return query_parameters


# ---------------------------------------------------------------------------
#   Content data validator
# ---------------------------------------------------------------------------


class PricingContentValidator(ContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = True
        status = data.get("status")

        if status == "Error":
            is_valid = False
            data["error_code"] = data.get("code")
            data["error_message"] = data.get("message")

        return is_valid


# ---------------------------------------------------------------------------
#   Data provider
# ---------------------------------------------------------------------------

pricing_data_provider = DataProvider(
    request=PricingRequestFactory(),
    response=PricingResponseFactory(),
    parser=ErrorParser(),
    validator=ValidatorContainer(content_validator=PricingContentValidator()),
)
