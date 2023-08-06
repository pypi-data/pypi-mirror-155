from concurrent.futures import Future, wait
from typing import TYPE_CHECKING, Dict, Any

from ._chain_record import create_chain_record, can_create_chain_record
from ..._content_type import ContentType
from ..._types import ExtendedParams, OptStr
from ....delivery._stream import StreamStateManager, OMMStreamListener
from ....delivery._stream._stream_factory import create_omm_stream

if TYPE_CHECKING:
    from ._chain_record import ChainRecord
    from ...._core.session import Session
    from ....delivery._stream import _OMMStream


class ChainRecords(StreamStateManager, OMMStreamListener["ChainRecords"]):
    def __init__(
        self,
        session: "Session",
        service: OptStr = None,
        extended_params: ExtendedParams = None,
    ):
        StreamStateManager.__init__(self, logger=session.logger())
        OMMStreamListener.__init__(self, logger=session.logger())
        self.display_template = None
        self.service: OptStr = service
        self.session: "Session" = session
        self.extended_params = extended_params
        self.records_by_name: Dict[str, "ChainRecord"] = {}
        self.refreshing_by_name: Dict[str, "Future"] = {}
        self.streams_by_name: Dict[str, "_OMMStream"] = {}

    def add(self, name: str):
        stream = create_omm_stream(
            ContentType.STREAMING_CHAINS,
            session=self.session,
            name=name,
            domain="MarketPrice",
            service=self.service,
            fields=[],
            extended_params=self.extended_params,
        )
        stream.on_refresh(self._on_stream_refresh)
        stream.on_status(self._on_stream_status)
        stream.on_update(self._on_stream_update)
        stream.on_complete(self._on_stream_complete)
        stream.on_error(self._on_stream_error)

        self.streams_by_name[name] = stream
        self.refreshing_by_name[name] = Future()
        self._debug(f"{self._classname} added stream for name: {name}")
        return stream

    def has(self, name: str) -> bool:
        return name in self.records_by_name

    def has_stream(self, name: str) -> bool:
        return name in self.streams_by_name

    def not_has_stream(self, name: str) -> bool:
        return not self.has_stream(name)

    def is_stream_close(self, name: str) -> bool:
        return self.streams_by_name[name].is_close

    def get_display_name(self, name: str) -> str:
        chain_record = self.records_by_name[name]
        return chain_record.display_name

    def _do_open(self, with_updates: bool):
        for stream in self.streams_by_name.values():
            self._debug(f"{self._classname} opens a stream with name {stream.name} [o]")
            stream.open(with_updates=with_updates)

    def _do_close(self):
        for refreshing in self.refreshing_by_name.values():
            if not refreshing.done():
                refreshing.set_result(1)

        for stream in self.streams_by_name.values():
            self._debug(
                f"{self._classname} closes a stream with name {stream.name} [c]"
            )
            stream.close()

    def open_stream(self, name: str, with_updates: bool):
        stream = self.streams_by_name[name]
        self._debug(f"{self._classname} opens a stream with name {stream.name} [c]")
        stream.open(with_updates=with_updates)

    def wait_refresh(self, name: str):
        wait([self.refreshing_by_name[name]])

    def get_record(self, name: str) -> "ChainRecord":
        record = self.records_by_name[name] if name in self.records_by_name else None
        return record

    def get_stream(self, name: str) -> "_OMMStream":
        return self.streams_by_name[name]

    def _do_on_stream_refresh(self, stream: "_OMMStream", *args) -> Any:
        message = args[0]
        fields = message.get("Fields", [])

        if can_create_chain_record(fields):
            chain_record = create_chain_record(fields)
            self._debug(f"{self._classname} created chain_record={chain_record}")
            self.records_by_name[stream.name] = chain_record

            if not self.display_template:
                self.display_template = chain_record.display_template

            refreshing = self.refreshing_by_name[stream.name]

            if not refreshing.done():
                refreshing.set_result(True)

        else:
            self._error(
                f"StreamingChain :: "
                f"Cannot parse chain {stream.name} because it is an invalid chain."
            )

        return message

    def _do_on_stream_status(self, originator, *args) -> Any:
        message = args[0]
        state = message.get("State", {})
        stream_state = state.get("Stream")
        if stream_state == "Closed":
            self.dispatch_error(originator, message)

        return message

    def _do_on_stream_error(self, originator: "_OMMStream", *args) -> Any:
        return originator.name, args

    def _do_on_stream_update(self, originator: "_OMMStream", *args) -> Any:
        return (originator,) + args
