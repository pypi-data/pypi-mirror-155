from ._data_provider import is_instrument_id, get_correct_symbol
from ._stream import CustomInstrumentsStream
from ...delivery._data._data_provider import DataProviderLayer
from ...delivery._data._endpoint_data import RequestMethod


class CustomInstrumentDataProviderLayer:
    def __init__(self, *args, **kwargs):
        self._data_provider_layer = DataProviderLayer(*args, **kwargs)

    def get_stream(self, session=None) -> CustomInstrumentsStream:
        universe = self._data_provider_layer._kwargs.get("universe")
        if is_instrument_id.match(universe):
            instrument_response = self._data_provider_layer.get_data(
                session, method=RequestMethod.GET
            )
            name = instrument_response.data.raw.get("symbol")
        else:
            name = get_correct_symbol(universe, session)
        stream = CustomInstrumentsStream(name, session=session)
        return stream
