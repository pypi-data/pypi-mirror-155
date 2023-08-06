# coding: utf-8

from typing import Callable, Optional, TYPE_CHECKING, Any

from ._protocol_type import ProtocolType
from ._stream_listener import OMMStreamListener, StreamEvent
from .stream import (
    Stream,
    update_message_with_extended_params,
)
from ...content._types import OptStr, ExtendedParams, Strings
from ..._tools import cached_property

if TYPE_CHECKING:
    from ._stream_factory import StreamDetails
    from . import StreamConnection
    from ..._core.session import Session


class _OMMStream(Stream, OMMStreamListener["_OMMStream"]):
    _message = None
    _code = None
    _with_updates: bool = True

    def __init__(
        self,
        stream_id: int,
        session: "Session",
        name: str,
        details: "StreamDetails",
        domain: OptStr = "MarketPrice",
        service: OptStr = None,
        fields: Optional[Strings] = None,
        key: Optional[dict] = None,
        extended_params: ExtendedParams = None,
        on_refresh: Optional[Callable] = None,
        on_status: Optional[Callable] = None,
        on_update: Optional[Callable] = None,
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
    ) -> None:
        Stream.__init__(self, stream_id, session, details)
        OMMStreamListener.__init__(
            self,
            logger=session.logger(),
            on_refresh=on_refresh,
            on_status=on_status,
            on_update=on_update,
            on_complete=on_complete,
            on_error=on_error,
        )
        self._name = name
        self._service = service
        self._fields = fields or []
        self._domain = domain
        self._key = key
        self._extended_params = extended_params

    @property
    def name(self) -> str:
        return self._name

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.OMM

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    @cached_property
    def open_message(self):
        open_message = {
            "ID": self.id,
            "Domain": self._domain,
            "Streaming": self._with_updates,
            "Key": {},
        }

        if self._key:
            open_message["Key"] = self._key

        open_message["Key"]["Name"] = self.name

        if self._service:
            open_message["Key"]["Service"] = self._service

        if self._fields:
            open_message["View"] = self._fields

        if self._extended_params:
            open_message = update_message_with_extended_params(
                open_message, self._extended_params
            )

        return open_message

    @cached_property
    def close_message(self):
        return {"ID": self.id, "Type": "Close"}

    def _do_open(self, *args, **kwargs):
        self._with_updates = kwargs.get("with_updates", True)

        self._initialize_cxn()

        self._cxn.on(self._event.refresh_by_id, self._on_stream_refresh)
        self._cxn.on(self._event.update_by_id, self._on_stream_update)
        self._cxn.on(self._event.status_by_id, self._on_stream_status)
        self._cxn.on(self._event.complete_by_id, self._on_stream_complete)
        self._cxn.on(self._event.error_by_id, self._on_stream_error)

        super()._do_open(*args, **kwargs)

    def _dispose(self):
        self._debug(f"{self._classname} disposing [d]")

        self._cxn.remove_listener(self._event.refresh_by_id, self._on_stream_refresh)
        self._cxn.remove_listener(self._event.update_by_id, self._on_stream_update)
        self._cxn.remove_listener(self._event.status_by_id, self._on_stream_status)
        self._cxn.remove_listener(self._event.complete_by_id, self._on_stream_complete)
        self._cxn.remove_listener(self._event.error_by_id, self._on_stream_error)

        self._release_cxn()
        self._debug(f"{self._classname} disposed [D]")

    def _do_on_stream_refresh(self, cxn: "StreamConnection", *args) -> Any:
        message = args[0]
        message_state = message.get("State", {})
        self._code = message_state.get("Stream", "")
        self._message = message_state.get("Text", "")
        return message

    def _on_stream_status(self, originator, *args) -> None:
        self._propagate_event(StreamEvent.STATUS, originator, *args)

        if self.is_open:
            self.dispatch_complete(originator, *args)

    def _do_on_stream_status(self, cxn: "StreamConnection", *args) -> Any:
        message = args[0]
        message_state = message.get("State", {})
        stream_state = message_state.get("Stream", "")
        code_state = message_state.get("Code", "")

        self._code = stream_state
        self._message = message_state.get("Text", "")

        if stream_state == "Closed":
            self._debug(
                f"{self._classname} received a closing message, "
                f"message_state={message_state}, state={self.state}"
            )

            if self.is_opening:
                self.dispatch_error(self, message)

            elif self.is_opened and code_state in {"AlreadyOpen", "NotEntitled"}:
                self.dispatch_error(self, message)

            elif self.is_closing:
                self._closed.set_result(True)

            else:
                raise ValueError(
                    f"{self._classname} Don't know what to do, state={self.state}, message={message}"
                )

        return message

    def _on_stream_complete(self, originator, *args) -> None:
        self._propagate_event(StreamEvent.COMPLETE, originator, *args)

        if self.is_opening:
            not self._opened.done() and self._opened.set_result(True)
