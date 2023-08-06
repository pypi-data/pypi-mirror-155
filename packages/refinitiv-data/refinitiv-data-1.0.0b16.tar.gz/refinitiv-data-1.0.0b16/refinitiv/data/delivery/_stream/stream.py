# coding: utf8
from concurrent.futures import Future, wait
from typing import Optional, Any
from typing import TYPE_CHECKING

from ._protocol_type import ProtocolType
from ._stream_cxn_cache import stream_cxn_cache
from .event import StreamEvent, StreamCxnEvent
from .stream_state import StreamState
from .stream_state_manager import StreamStateManager
from ..._core.session.tools import is_closed

if TYPE_CHECKING:
    from ...content._content_type import ContentType
    from .._stream import StreamConnection
    from ..._core.session import Session
    from ._stream_factory import StreamDetails


class Stream(StreamStateManager):
    _cxn: Optional["StreamConnection"] = None
    _event: Optional[StreamEvent] = None

    def __init__(
        self,
        stream_id: int,
        session: "Session",
        details: "StreamDetails",
    ) -> None:
        StreamStateManager.__init__(self, logger=session.logger())
        self.details = details
        self._id: int = stream_id
        self._session: "Session" = session
        self._opened: Optional[Future] = None
        self._closed: Optional[Future] = None
        self._classname = f"[{self.__class__.__name__}_{self.id}]"

    @property
    def classname(self):
        return self._classname

    @property
    def id(self) -> int:
        return self._id

    @property
    def session(self) -> "Session":
        return self._session

    @property
    def name(self) -> str:
        return ""

    @property
    def content_type(self) -> "ContentType":
        return self.details.content_type

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.NONE

    @property
    def close_message(self) -> dict:
        return {}

    @property
    def open_message(self) -> dict:
        return {}

    def open(self, *args, with_updates: bool = True) -> StreamState:
        if is_closed(self._session):
            raise AssertionError("Session must be open")

        return super().open(with_updates=with_updates)

    def send(self, message) -> None:
        self._debug(f"{self._classname} send message={message}")
        self._cxn.send(message)

    def _initialize_cxn(self):
        self._event = StreamEvent.get(self.id)
        self._cxn = stream_cxn_cache.get_cxn(self.session, self.details)
        self._cxn.on(StreamCxnEvent.DISCONNECTING, self.close)
        self._cxn.on(StreamCxnEvent.RECONNECTED, self._on_reconnected)
        self._cxn.on(StreamCxnEvent.DISPOSED, self.halt)

    def _release_cxn(self):
        self._cxn.remove_listener(StreamCxnEvent.DISCONNECTING, self.close)
        self._cxn.remove_listener(StreamCxnEvent.RECONNECTED, self._on_reconnected)
        self._cxn.remove_listener(StreamCxnEvent.DISPOSED, self.halt)
        self._debug(f"{self._classname} release cxn={self._cxn}")
        stream_cxn_cache.release(self.session, self.details)
        self._cxn = None

    def _do_open(self, *args, **kwargs) -> None:
        self._opened = Future()
        self.send(self.open_message)
        wait([self._opened])

    def _do_close(self, *args, **kwargs):
        self._closed = Future()
        self.send(self.close_message)
        self._dispose()

    def _on_reconnected(self, *args, **kwargs):
        if self.is_open:
            self.send(self.open_message)

    def _do_on_stream_error(self, originator, *args) -> Any:
        if self.is_opening:
            not self._opened.done() and self._opened.set_result(False)

        return args


def update_message_with_extended_params(message: dict, extended_params: dict) -> dict:
    return update_key_in_dict(message, extended_params)


def update_key_in_dict(message: dict, extended_params: dict) -> dict:
    for param, extended_val in extended_params.items():
        if param in message:
            prev_value = message[param]
            if isinstance(prev_value, dict) and isinstance(extended_val, dict):
                update_key_in_dict(prev_value, extended_val)
            else:
                message[param] = extended_val
        else:
            message[param] = extended_val

    return message
