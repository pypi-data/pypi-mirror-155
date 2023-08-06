from typing import Union, TYPE_CHECKING
from ..._open_state import OpenState
from .stream_state import StreamState

if TYPE_CHECKING:
    from ...content.ipa.financial_contracts._quantitative_data_stream import (
        QuantitativeDataStream,
    )
    from ...content.trade_data_service._stream import TradeDataStream
    from ...content.pricing.chain._stream import StreamingChain
    from . import OMMStream, RDPStream
    from ...content._streamingprices import StreamingPrices

    Stream = Union[
        StreamingPrices,
        StreamingChain,
        TradeDataStream,
        RDPStream,
        OMMStream,
        QuantitativeDataStream,
    ]

stream_state_to_open_state = {
    StreamState.Opened: OpenState.Opened,
    StreamState.Opening: OpenState.Pending,
    StreamState.Paused: OpenState.Pending,
    StreamState.Pausing: OpenState.Pending,
    StreamState.Closed: OpenState.Closed,
    StreamState.Closing: OpenState.Pending,
}


class StreamOpenMixin(object):
    _stream: "Stream" = None

    @property
    def open_state(self) -> OpenState:
        return stream_state_to_open_state.get(self._stream.state)

    def open(self) -> OpenState:
        self._stream.open()
        return self.open_state

    async def open_async(self) -> OpenState:
        await self._stream.open_async()
        return self.open_state

    def close(self) -> OpenState:
        self._stream.close()
        return self.open_state


class StreamOpenWithUpdatesMixin(StreamOpenMixin):
    def open(self, with_updates: bool = True) -> OpenState:
        self._stream.open(with_updates=with_updates)
        return self.open_state

    async def open_async(self, with_updates: bool = True) -> OpenState:
        await self._stream.open_async(with_updates=with_updates)
        return self.open_state
