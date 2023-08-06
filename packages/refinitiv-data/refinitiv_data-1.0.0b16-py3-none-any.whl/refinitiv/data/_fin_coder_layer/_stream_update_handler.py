import abc
from datetime import datetime
from typing import TYPE_CHECKING, Callable

from ._recording_control import RecordMixin
from ..delivery._stream import StreamEvent

if TYPE_CHECKING:
    from ..content._types import OptDict
    from ._ohlc_builder import Ticks_OHLCBuilder
    from ..content._streamingprices import StreamingPrice, StreamingPrices


class StreamUpdateHandler(abc.ABC):
    updates_by_stream_name: "OptDict" = None

    @abc.abstractmethod
    def start_handling(self):
        pass

    @abc.abstractmethod
    def stop_handling(self):
        pass

    @abc.abstractmethod
    def dispose(self):
        pass


class CollectUpdates_StreamUpdateHandler(StreamUpdateHandler):
    def __init__(self, stream: "StreamingPrices", recorder: "PricingRecorder") -> None:
        self.stream = stream
        self.updates_by_stream_name = {}
        self._frequency = recorder._frequency
        self._ticks_per_bar = recorder._ticks_per_bar
        self._on_data_callback = recorder._on_data
        self._recorder = recorder

    def start_handling(self):
        for universe in self.stream.universe:
            stream: "StreamingPrice" = self.stream._streaming_prices_by_name[universe]
            stream._stream.on(StreamEvent.UPDATE, self._on_update_handler)
            stream._stream.on(StreamEvent.REFRESH, self._on_update_handler)

    def stop_handling(self):
        for universe in self.stream.universe:
            stream: "StreamingPrice" = self.stream._streaming_prices_by_name[universe]
            stream._stream.off(StreamEvent.UPDATE, self._on_update_handler)
            stream._stream.off(StreamEvent.REFRESH, self._on_update_handler)

    def dispose(self):
        self.updates_by_stream_name = {}

    def _on_update_handler(self, stream: "StreamingPrice", message: dict):
        message["Timestamp"] = datetime.now()

        updates = self.updates_by_stream_name.setdefault(stream.name, [])
        updates.append(message)

        if (
            self._frequency == "tick"
            and self._ticks_per_bar == 1
            and self._on_data_callback
        ):
            self._on_data_callback(message, self._recorder)

        self._do_on_update_handler(stream, message)

    def _do_on_update_handler(self, stream: "StreamingPrice", message: dict):
        # for override
        pass


class BuildDF_StreamUpdateHandler(CollectUpdates_StreamUpdateHandler, RecordMixin):
    def __init__(
        self,
        stream: "StreamingPrices",
        ohlc_builder: "Ticks_OHLCBuilder",
        ticks_per_bar: int,
        recorder: "PricingRecorder",
        on_record_callback: Callable = None,
    ) -> None:
        super().__init__(stream, recorder)
        self.ohlc_builder = ohlc_builder
        self.ticks_per_bar = ticks_per_bar
        self.counter = 0
        self.update_handler = self
        self.on_record_callback = on_record_callback
        self._recorder = recorder

    def _do_on_update_handler(self, stream: "StreamingPrice", message: dict):
        self.counter += 1

        if self.counter == self.ticks_per_bar:
            self.record()
            self.counter = 0
