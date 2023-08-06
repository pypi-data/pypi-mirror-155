from refinitiv.data._tools import cached_property


class StreamStateEvent:
    OPENING = "opening_state_event"
    OPENED = "opened_state_event"
    CLOSING = "closing_state_event"
    CLOSED = "closed_state_event"
    PAUSING = "pausing_state_event"
    PAUSED = "paused_state_event"


class StreamEvent:
    # broadcast events
    UPDATE = "update_stream_event"
    REFRESH = "refresh_stream_event"
    STATUS = "status_stream_event"
    COMPLETE = "complete_stream_event"
    ERROR = "error_stream_event"
    ACK = "ack_stream_event"
    RESPONSE = "response_stream_event"
    ALARM = "alarm_stream_event"

    # specific events
    _UPDATE = "update_stream_{}_event"
    _REFRESH = "refresh_stream_{}_event"
    _STATUS = "status_stream_{}_event"
    _COMPLETE = "complete_stream_{}_event"
    _ERROR = "error_stream_{}_event"
    _ACK = "ack_stream_{}_event"
    _RESPONSE = "response_stream_{}_event"
    _ALARM = "alarm_stream_{}_event"

    _cache = {}

    def __init__(self, stream_id) -> None:
        self.stream_id = stream_id

    @cached_property
    def update_by_id(self) -> str:
        return self._UPDATE.format(self.stream_id)

    @cached_property
    def refresh_by_id(self) -> str:
        return self._REFRESH.format(self.stream_id)

    @cached_property
    def status_by_id(self) -> str:
        return self._STATUS.format(self.stream_id)

    @cached_property
    def complete_by_id(self) -> str:
        return self._COMPLETE.format(self.stream_id)

    @cached_property
    def error_by_id(self) -> str:
        return self._ERROR.format(self.stream_id)

    @cached_property
    def ack_by_id(self) -> str:
        return self._ACK.format(self.stream_id)

    @cached_property
    def response_by_id(self) -> str:
        return self._RESPONSE.format(self.stream_id)

    @cached_property
    def alarm_by_id(self) -> str:
        return self._ALARM.format(self.stream_id)

    @classmethod
    def get(cls, stream_id: int) -> "StreamEvent":
        event = cls._cache.setdefault(stream_id, StreamEvent(stream_id))
        return event


class StreamCxnEvent(object):
    # broadcast events
    CONNECTING = "connecting_cxn_event"
    CONNECTED = "connected_cxn_event"
    READY = "ready_cxn_event"
    DISCONNECTING = "disconnecting_cxn_event"
    DISCONNECTED = "disconnected_cxn_event"
    DISPOSED = "disposed_cxn_event"
    RECONNECTING = "reconnecting_cxn_event"
    RECONNECTED = "reconnected_cxn_event"
