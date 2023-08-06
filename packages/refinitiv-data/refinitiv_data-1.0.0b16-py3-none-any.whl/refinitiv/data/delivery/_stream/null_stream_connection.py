from typing import Callable

from . import StreamConnection
from ._stream_cxn_config import NullStreamCxnConfig
from ..._core.session.null_session import NullSession


class NullStreamConnection(StreamConnection):
    def __init__(self):
        StreamConnection.__init__(
            self,
            connection_id=-1,
            name="",
            session=NullSession(),
            config=NullStreamCxnConfig(),
            max_reconnect=0,
        )

    @property
    def can_run(self):
        return False

    @property
    def is_ready(self):
        return False

    @property
    def is_disposed(self):
        return False

    @property
    def can_be_disconnect(self):
        return False

    def connect(self):
        # do nothing
        pass

    def disconnect(self):
        # do nothing
        pass

    def dispose(self):
        # do nothing
        pass

    def send(self, data: dict) -> None:
        # do nothing
        pass

    def on(self, event: str, listener: Callable) -> None:
        # do nothing
        pass

    def remove_listener(self, event: str, listener: Callable) -> None:
        # do nothing
        pass
