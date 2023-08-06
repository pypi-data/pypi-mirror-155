# coding: utf8
import itertools
import re
from typing import Tuple, Any

from .._content_type import ContentType
from ..._core.session._default_session_manager import get_valid_session
from ...delivery._stream import (
    StreamStateEvent,
    StreamStateManager,
    OMMStreamListener,
    _OMMStream,
)
from ...delivery._stream._stream_factory import create_omm_stream
from ...delivery._stream.stream_cache import StreamCache
from ..._tools import cached_property, DEBUG

# regular expression pattern for intra-field position sequence
_partial_update_intra_field_positioning_sequence_regular_expression_pattern = (
    r"[\x1b\x5b|\x9b]([0-9]+)\x60([^\x1b^\x5b|^\x9b]+)"
)
_huge = 1e12


def _decode_intra_field_position_sequence(cached_value, new_value):
    # find all partial update in the value
    tokens = re.findall(
        _partial_update_intra_field_positioning_sequence_regular_expression_pattern,
        new_value,
    )

    # check this value contains a partial update or not?
    if len(tokens) == 0:
        # no partial update required, so done
        return new_value

    # do a partial update
    updated_value = cached_value
    for (offset, replace) in tokens:
        # convert offset from str to int
        offset = int(offset)
        assert offset < len(updated_value)

        # replace the value in the string
        updated_value = (
            updated_value[:offset] + replace + updated_value[offset + len(replace) :]
        )

    # done, return
    return updated_value


_id_iterator = itertools.count()


class StreamingPrice(
    StreamCache, StreamStateManager, OMMStreamListener["StreamingPrice"]
):
    def __init__(
        self,
        name,
        session=None,
        fields=None,
        service=None,
        extended_params=None,
        on_refresh=None,
        on_status=None,
        on_update=None,
        on_complete=None,
        on_error=None,
        parent_id=None,
    ):
        if name is None:
            raise AttributeError("Instrument name must be defined.")

        session = get_valid_session(session)

        StreamCache.__init__(self, name=name, fields=fields, service=service)
        StreamStateManager.__init__(self, logger=session.logger())
        OMMStreamListener.__init__(
            self,
            logger=session.logger(),
            on_refresh=on_refresh,
            on_status=on_status,
            on_update=on_update,
            on_complete=on_complete,
            on_error=on_error,
        )

        self._id = next(_id_iterator)
        if parent_id is not None:
            id_ = f"{parent_id}.{self._id}"
        else:
            id_ = f"{self._id}"

        self._classname: str = f"[{self.__class__.__name__}_{id_} name='{name}']"
        self._session = session
        self._extended_params = extended_params
        self._record = {}

    @cached_property
    def _stream(self) -> _OMMStream:
        omm_stream = create_omm_stream(
            ContentType.STREAMING_PRICING,
            session=self._session,
            name=self._name,
            domain="MarketPrice",
            service=self._service,
            fields=self._fields,
            extended_params=self._extended_params,
            on_refresh=self._on_stream_refresh,
            on_status=self._on_stream_status,
            on_update=self._on_stream_update,
            on_complete=self._on_stream_complete,
            on_error=self._on_stream_error,
        )
        omm_stream.on(StreamStateEvent.CLOSED, self.close)
        return omm_stream

    @property
    def id(self) -> int:
        return self._stream.id

    @property
    def code(self):
        return self._stream.code

    @property
    def message(self):
        return self._stream.message

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def _do_pause(self):
        self._stream.pause()

    def _do_resume(self):
        self._stream.resume()

    def _do_close(self, *args, **kwargs):
        id_ = self._stream.id
        self._debug(f"{self._classname} Stop subscription {id_} to {self.name}")
        self._stream.close(*args, **kwargs)

    def _do_open(self, *args, with_updates=True):
        id_ = self._stream.id
        self._debug(f"{self._classname} Open async {id_} to {self.name}")
        self._stream.open(*args, with_updates=with_updates)

    def _decode_partial_update_field(self, key, value):
        """
        This legacy is used to process the partial update
        RETURNS the processed partial update data
        """

        fields = self._record.get("Fields")
        if key not in fields:
            fields[key] = value
            self._warning(f"key {key} not in self._record['Fields']")
            return value

        # process infra-field positioning sequence
        cached_value = fields[key]
        updated_value = _decode_intra_field_position_sequence(cached_value, value)

        # done
        return updated_value

    def _write_to_record(self, message: dict):
        for data in message:
            if data == "Fields":
                fields = message[data]
                # fields data
                # loop over all update items
                for key, value in fields.items():
                    # only string value need to check for a partial update
                    if isinstance(value, str):
                        # value is a string, so check for partial update string
                        # process partial update and update the callback
                        # with processed partial update
                        fields[key] = self._decode_partial_update_field(key, value)

                # update the field data
                self._record.setdefault(data, {})
                self._record[data].update(fields)
            else:
                # not a "Fields" data
                self._record[data] = message[data]

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

        fields = message.get("Fields")
        return fields

    def _do_on_stream_status(self, stream: "_OMMStream", *args) -> Any:
        message = args[0]
        self._status = message
        return message

    def _do_on_stream_update(self, stream: "_OMMStream", *args) -> Any:
        message = args[0]

        if DEBUG:
            fields = self._record.get("Fields", [])
            num_fields = len(fields)
            self._debug(
                f"|>|>|>|>|>|> {self._classname} "
                f"has fields in record {num_fields} after update"
            )

        self._write_to_record(message)
        fields = message.get("Fields")
        return fields
