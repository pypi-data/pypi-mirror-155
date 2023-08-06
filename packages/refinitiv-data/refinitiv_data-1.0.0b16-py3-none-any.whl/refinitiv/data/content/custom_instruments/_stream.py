import itertools
from typing import (
    Union,
    Callable,
    Iterable,
    Tuple,
    TYPE_CHECKING,
)

import pandas as pd

from .._content_type import ContentType
from ..._core.session import get_valid_session, Session
from ..._tools import DEBUG, cached_property, PRICING_DATETIME_PATTERN
from ..._tools._dataframe import convert_df_columns_to_datetime_use_re_compile
from ...delivery._stream import (
    StreamStateManager,
    OMMStreamListener,
    StreamStateEvent,
    _OMMStream,
    StreamState,
)
from ...delivery._stream._stream_factory import create_omm_stream
from ...delivery._stream.base_stream import stream_state_to_open_state
from ...delivery._stream.stream_cache import StreamCache

if TYPE_CHECKING:
    from ... import OpenState

_id_iterator = itertools.count()


class CustomInstrumentsStream(
    StreamCache, StreamStateManager, OMMStreamListener["CustomInstrumentsStream"]
):
    def __init__(
        self,
        name: Union[str, Iterable[str]],
        session: "Session" = None,
        service=None,
        on_refresh: Callable = None,
        on_status: Callable = None,
        on_update: Callable = None,
        on_complete: Callable = None,
        extended_params: dict = None,
    ):
        if name is None:
            raise AttributeError("universe name must be defined.")

        session = get_valid_session(session)

        StreamCache.__init__(self, name=name, service=service)
        StreamStateManager.__init__(self, logger=session.logger())
        OMMStreamListener.__init__(
            self,
            logger=session.logger(),
            on_refresh=on_refresh,
            on_status=on_status,
            on_update=on_update,
            on_complete=on_complete,
        )

        self._session = session
        self._name = name
        self._extended_params = extended_params
        self._record = {}

    @cached_property
    def _stream(self):
        stream = create_omm_stream(
            ContentType.STREAMING_CUSTOM_INSTRUMENTS,
            session=self._session,
            name=self._name,
            domain="MarketPrice",
            extended_params=self._extended_params,
            on_refresh=self._on_stream_refresh,
            on_status=self._on_stream_status,
            on_update=self._on_stream_update,
            on_complete=self._on_stream_complete,
            on_error=self._on_stream_error,
        )
        stream.on(StreamStateEvent.CLOSED, self.close)
        return stream

    def _do_on_stream_update(self, stream: _OMMStream, *args):
        message = args[0]

        if DEBUG:
            fields = self._record.get("Fields", [])
            num_fields = len(fields)
            self._debug(
                f"|>|>|>|>|>|> {self._classname} "
                f"has fields in record {num_fields} after update"
            )

        fields = message.get("Fields")
        self._record["Fields"].update(fields)
        return fields

    def _do_open(self, *args, with_updates=True):
        self._stream.open(*args, with_updates=with_updates)

    def _do_pause(self):
        self._stream.pause()

    def _do_resume(self):
        self._stream.resume()

    def _do_close(self, *args, **kwargs):
        self._stream.close(*args, **kwargs)

    def _do_on_stream_refresh(self, stream: "_OMMStream", *args) -> Tuple:
        message = args[0]
        self._record = message

        if DEBUG:
            fields = self._record.get("Fields", [])
            num_fields = len(fields)
            self._debug(
                f"|>|>|>|>|>|>{self._classname} "
                f"has fields in record {num_fields} after refresh"
            )

        fields = message.get("Fields", {})
        return fields

    def get_snapshot(self):
        fields = self._record.get("Fields")
        df = pd.DataFrame(fields, index=[self._name])
        convert_df_columns_to_datetime_use_re_compile(df, PRICING_DATETIME_PATTERN)
        return df

    @property
    def open_state(self) -> "OpenState":
        state: "StreamState" = self._stream.state
        state: "OpenState" = stream_state_to_open_state.get(state)
        return state
