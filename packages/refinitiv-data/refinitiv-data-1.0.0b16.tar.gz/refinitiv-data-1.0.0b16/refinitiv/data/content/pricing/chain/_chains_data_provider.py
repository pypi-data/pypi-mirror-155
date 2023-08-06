# coding: utf-8

from pandas import DataFrame

from ....delivery._data._data_provider import (
    DataProvider,
    RequestFactory,
)

# ---------------------------------------------------------------------------
#   Content data
# ---------------------------------------------------------------------------

_response_universe_name = "universe"
_response_ric_name = "ric"
_response_display_name_name = "displayName"
_response_service_name_name = "serviceName"
_response_data_name = "data"
_response_constituents_name = "constituents"


def chains_build_df(raw, **kwargs):
    universe = raw[_response_universe_name]
    ric = universe[_response_ric_name]
    data = raw[_response_data_name]
    constituents = data[_response_constituents_name]
    _df = None
    if len(constituents):
        _df = DataFrame({ric: constituents})
    else:
        _df = DataFrame([], columns=[ric])
    if not _df.empty:
        _df = _df.convert_dtypes()
    return _df


# ---------------------------------------------------------------------------
#   Request factory
# ---------------------------------------------------------------------------


class ChainsRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        url = args[1]
        url = url + "?universe={universe}"
        return url

    def get_path_parameters(self, *_, **kwargs):
        universe = kwargs.get("universe")
        if universe is None:
            return {}
        return {"universe": universe}


# ---------------------------------------------------------------------------
#   Data provider
# ---------------------------------------------------------------------------

chains_data_provider = DataProvider(
    request=ChainsRequestFactory(),
)
