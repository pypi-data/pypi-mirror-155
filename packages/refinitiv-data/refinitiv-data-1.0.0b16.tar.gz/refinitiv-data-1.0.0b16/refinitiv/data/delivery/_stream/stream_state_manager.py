import asyncio
from functools import partial
from typing import TYPE_CHECKING

from pyee import EventEmitter

from .event import StreamStateEvent
from .stream_state import StreamState
from ..._core.log_reporter import _LogReporter
from ..._tools import cached_property

if TYPE_CHECKING:
    from logging import Logger


class StreamStateManager(_LogReporter):
    def __init__(self, logger: "Logger") -> None:
        _LogReporter.__init__(self, logger=logger)
        self._prev_state = None

        if not hasattr(self, "_classname"):
            self._classname: str = self.__class__.__name__

        self._state = StreamState.Closed

    @cached_property
    def _emitter(self) -> EventEmitter:
        return EventEmitter()

    @property
    def state(self) -> StreamState:
        return self._state

    def on(self, event, listener):
        return self._emitter.on(event, listener)

    def off(self, event, listener):
        return self._emitter.remove_listener(event, listener)

    @property
    def is_opened(self) -> bool:
        return self.state is StreamState.Opened

    @property
    def is_opening(self) -> bool:
        return self.state is StreamState.Opening

    @property
    def is_open(self) -> bool:
        return self.is_opened or self.is_opening

    @property
    def is_paused(self) -> bool:
        return self.state is StreamState.Paused

    @property
    def is_pausing(self) -> bool:
        return self.state is StreamState.Pausing

    @property
    def is_close(self) -> bool:
        return self.is_closed or self.is_closing

    @property
    def is_closing(self) -> bool:
        return self.state is StreamState.Closing

    @property
    def is_closed(self) -> bool:
        return self.state is StreamState.Closed

    def open(self, *args, **kwargs) -> StreamState:
        if self.is_opening or self.is_opened:
            self._warning(f"{self._classname} can’t open, state={self.state}")
            return self.state

        self._debug(f"{self._classname} is opening [o]")
        self._state = StreamState.Opening
        self._emitter.emit(StreamStateEvent.OPENING, self)
        self._do_open(*args, **kwargs)
        self._state = StreamState.Opened
        self._emitter.emit(StreamStateEvent.OPENED, self)
        self._debug(f"{self._classname} opened [O]")
        return self.state

    async def open_async(self, *args, **kwargs) -> StreamState:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, partial(self.open, *args, **kwargs))
        return result

    def _do_open(self, *args, **kwargs):
        # for override
        pass

    def close(self, *args, **kwargs) -> StreamState:
        if self.is_closing or self.is_closed:
            return self.state

        self._debug(f"{self._classname} is closing [c]")
        self._state = StreamState.Closing
        self._emitter.emit(StreamStateEvent.CLOSING, self)
        self._do_close(*args, **kwargs)
        self._state = StreamState.Closed
        self._emitter.emit(StreamStateEvent.CLOSED, self)
        self._debug(f"{self._classname} closed [C]")
        return self.state

    async def close_async(self, *args, **kwargs) -> StreamState:
        return self.close(*args, **kwargs)

    def _do_close(self, *args, **kwargs):
        # for override
        pass

    def halt(self, *args) -> StreamState:
        if self.is_closing or self.is_closed:
            return self.state

        self._debug(f"{self._classname} halt")
        self._dispose()
        return self.state

    def _dispose(self):
        # for override
        pass

    def pause(self):
        if self.is_paused or self.is_pausing:
            return self.state

        self._set_pause()
        self._do_pause()

        return self.state

    def _set_pause(self):
        self._prev_state = self.state
        self._state = StreamState.Paused

    def _do_pause(self):
        # for override
        pass

    def resume(self):
        if self.is_paused:
            self._set_resume()
            self._do_resume()
        return self.state

    def _set_resume(self):
        self._state = self._prev_state

    def _do_resume(self):
        # for override
        pass
