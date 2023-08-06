# coding: utf-8

import json
import os
import queue
import threading
import traceback
from concurrent.futures import Future
from typing import Callable, Dict, List, Optional, TYPE_CHECKING, Union

import websocket
from pyee import EventEmitter

from .event import StreamCxnEvent
from .rwf.socket import RwfSocketApp
from .stream_cxn_state import StreamCxnState
from ..._core.log_reporter import LogReporter
from ..._core.session import SessionType
from ..._core.session.tools import get_delays
from ..._tools import DEBUG

if TYPE_CHECKING:
    from ._stream_cxn_config import StreamCxnConfig
    from ..._core.session import Session

LOGIN_STREAM_ID = 2
MAX_LISTENERS = 2000
WAIT_TIMEOUT_FOR_CLOSE_MESSAGE_FROM_WS_SERVER = 1
delays = get_delays()


class StreamConnection(threading.Thread, LogReporter):
    _listener: Optional[Union[websocket.WebSocketApp, RwfSocketApp]] = None
    _num_reconnect = 0

    def __init__(
        self,
        connection_id: int,
        name: str,
        session: "Session",
        config: "StreamCxnConfig",
        max_reconnect: int,
    ) -> None:
        self._id: int = connection_id
        self._session: "Session" = session
        self._config: "StreamCxnConfig" = config

        LogReporter.__init__(self, logger=session.logger())
        threading.Thread.__init__(
            self, target=self.connect, name=f"Thread{name}", daemon=True
        )

        self._state: StreamCxnState = StreamCxnState.Initial
        self._is_emit_reconnected: bool = False

        self._is_auto_reconnect: bool = self._session.stream_auto_reconnection
        self._max_reconnect: int = max_reconnect

        self._emitter: EventEmitter = EventEmitter()
        self._emitter.max_listeners = MAX_LISTENERS

        self.prepared: Future = Future()
        self.closed: Future = Future()
        self._timer = threading.Event()

        self._msg_queue: Optional[queue.Queue] = None
        self._msg_processor: Optional[threading.Thread] = None

        self._classname = f"[{name}]"

    @property
    def session(self) -> "Session":
        return self._session

    @property
    def id(self) -> int:
        return self._id

    @property
    def state(self) -> StreamCxnState:
        return self._state

    @property
    def subprotocol(self) -> str:
        return ""

    @property
    def can_connect(self) -> bool:
        return self.state in {StreamCxnState.Reconnecting, StreamCxnState.Initial}

    @property
    def is_connecting(self) -> bool:
        return self.state is StreamCxnState.Connecting

    @property
    def is_connected(self) -> bool:
        return self.state is StreamCxnState.Connected

    @property
    def is_ready(self) -> bool:
        return self.state is StreamCxnState.Ready

    @property
    def can_disconnect(self) -> bool:
        return self.is_ready or self.is_connected or self.is_connecting

    @property
    def is_disconnecting(self) -> bool:
        return self.state is StreamCxnState.Disconnecting

    @property
    def is_disposed(self) -> bool:
        return self.state is StreamCxnState.Disposed

    @property
    def can_reconnect(self) -> bool:
        if self.session.server_mode and self._is_auto_reconnect:
            return True

        if self.session.server_mode and not self._is_auto_reconnect:
            return False

        if not self.session.server_mode and self._is_auto_reconnect:
            num_urls = len(self._config.urls)
            if self._num_reconnect >= self._max_reconnect * num_urls:
                return False
            else:
                return True
        else:
            return False

    def connect(self) -> None:
        if self.is_connecting or self.is_connected:
            self.debug(f"{self._classname} can’t connect, state={self.state}")
            return

        self.debug(f"{self._classname} is connecting [con]")

        self._state = StreamCxnState.Connecting
        self._emitter.emit(StreamCxnEvent.CONNECTING, self)

        self._msg_queue = queue.Queue()
        self._msg_processor = threading.Thread(
            target=self._process_messages, name=f"Msg-Proc-{self.name}", daemon=True
        )
        self._msg_processor.start()

        if self._config.transport == "tcp":
            self._run_tcp_listener()
        else:
            self._run_websocket_listener()

    def _run_tcp_listener(self):
        def on_open(app):
            self._on_ws_open(app)
            self._state = StreamCxnState.Ready
            self.prepared.set_result(True)

        host, port = self._config.url.split(":")
        port = int(port) if port else None

        cfg = self._session.config
        cfg_prefix = "apis.streaming.pricing"
        field_dict_path = cfg.get(f"{cfg_prefix}.field_dict_path")
        enumtype_path = cfg.get(f"{cfg_prefix}.enumtype_path")

        self.debug(
            f"{self._classname} connect (\n"
            f"\tnum_connect={self._num_reconnect},\n"
            f"\turl={self._config.url},\n"
            f"\ttransport={self._config.transport},\n"
        )

        self._listener = RwfSocketApp(
            host=host,
            port=port,
            field_dict_path=field_dict_path,
            enumtype_path=enumtype_path,
            on_open=on_open,
            on_msg=self._on_ws_message,
            on_close=self._on_ws_close,
        )

        self._listener.run_forever(self.get_login_message())

    def _run_websocket_listener(self):
        if DEBUG:
            websocket.enableTrace(True)

        cookie = None
        user_id = os.getenv("REFINITIV_AAA_USER_ID")
        if self._session.type == SessionType.DESKTOP and user_id:
            cookie = f"user-uuid={user_id}"

        headers = ["User-Agent: Python"] + self._config.headers
        subprotocols = [self.subprotocol]

        self.debug(
            f"{self._classname} connect (\n"
            f"\tnum_connect={self._num_reconnect},\n"
            f"\turl={self._config.url},\n"
            f"\theaders={headers},\n"
            f"\tcookies={cookie},\n"
            f"\ttransport={self._config.transport},\n"
            f"\tsubprotocols={subprotocols})"
        )

        self._listener = websocket.WebSocketApp(
            url=self._config.url,
            header=headers,
            cookie=cookie,
            on_open=self._on_ws_open,
            on_message=self._on_ws_message,
            on_error=self._on_ws_error,
            on_close=self._on_ws_close,
            on_ping=self._on_ws_ping,
            on_pong=self._on_ws_pong,
            subprotocols=subprotocols,
        )

        proxy_config = self._config.proxy_config
        http_proxy_host = None
        http_proxy_port = None
        http_proxy_auth = None
        proxy_type = None
        if proxy_config:
            http_proxy_host = proxy_config.host
            http_proxy_port = proxy_config.port
            http_proxy_auth = proxy_config.auth
            proxy_type = proxy_config.type

        no_proxy = self._config.no_proxy

        self._listener.run_forever(
            http_proxy_host=http_proxy_host,
            http_proxy_port=http_proxy_port,
            http_proxy_auth=http_proxy_auth,
            http_no_proxy=no_proxy,
            proxy_type=proxy_type,
            skip_utf8_validation=True,
        )

    def disconnect(self) -> None:
        if self.is_disconnecting or self.is_disposed:
            self.debug(f"{self._classname} can’t disconnect, state={self.state}")
            return

        self.debug(f"{self._classname} is disconnecting [dis]")
        self._state = StreamCxnState.Disconnecting
        self.prepared.cancel()
        self._emitter.emit(StreamCxnEvent.DISCONNECTING, self)
        self.debug(f"{self._classname} disconnected [DIS]")

    def dispose(self) -> None:
        if self.is_disposed:
            self.debug(f"{self._classname} can’t dispose, state={self.state}")
            return

        self.debug(f"{self._classname} is disposing [d]")

        close_message = self.get_close_message()
        if close_message and not self.is_connecting:
            self.send(close_message)

        self._state = StreamCxnState.Disposed

        self._listener.close()
        self._listener = None

        self._msg_queue = None
        self._msg_processor = None

        if not self.prepared.done():
            self.prepared.set_result(False)
        self.closed.set_result(True)
        self.prepared.cancel()
        self.closed.cancel()
        self._emitter.emit(StreamCxnEvent.DISPOSED, self)
        self.debug(f"{self._classname} disposed [D]")

    def get_login_message(self) -> dict:
        # for override
        pass

    def get_close_message(self) -> dict:
        # for override
        pass

    def send_login_message(self) -> None:
        login_message = self.get_login_message()
        self.send(login_message)

    def send(self, data: dict) -> None:
        s = json.dumps(data)
        self.debug(f"{self._classname} send s={s}")
        self._listener.send(s)

    def on(self, event: str, listener: Callable) -> None:
        self._emitter.on(event, listener)

    def remove_listener(self, event: str, listener: Callable) -> None:
        self._emitter.remove_listener(event, listener)

    def _on_ws_open(self, ws: websocket.WebSocketApp) -> None:
        self.debug(f"{self._classname} connected [CON]")
        self.debug(f"{self._classname} on_ws_open")

        self._state = StreamCxnState.Connected

        delays.reset()

        self._emitter.emit(StreamCxnEvent.CONNECTED, self)

        login_message = self.get_login_message()
        self.send(login_message)

    def _on_ws_message(self, ws: websocket.WebSocketApp, s: str) -> None:
        self.debug(f"{self._classname} on_ws_message {s}")

        try:
            messages = json.loads(s)
        except UnicodeDecodeError:
            messages = "".join(map(chr, [byte for byte in bytearray(s)]))
            messages = json.loads(messages)

        if self.is_connected:
            if len(messages) > 1:
                raise ValueError(
                    f"Cannot process messages more then one, num={len(messages)}"
                )

            message = messages[0]
            self._handle_login_message(message)

            if self._is_emit_reconnected:
                self.debug(f"Reconnecting is over, emit event Reconnected.")
                self._is_emit_reconnected = False
                self._emitter.emit(StreamCxnEvent.RECONNECTED, self)

        elif self.is_ready or self.is_disconnecting:
            self._msg_queue.put(messages)

        else:
            debug_msg = (
                f"{self._classname} _on_ws_message: "
                f"don't know what to do, {self.state}, "
                f"message={messages}"
            )
            if DEBUG:
                raise ValueError(debug_msg)

            else:
                self.error(debug_msg)

    def _handle_login_message(self, message: dict):
        # for override
        pass

    def _process_messages(self) -> None:
        while not self.is_disposed:
            messages: List[Dict] = self._msg_queue.get()
            for message in messages:
                self._process_message(message)
            self._msg_queue.task_done()

    def _process_message(self, message: dict) -> None:
        # for override
        pass

    def _on_ws_close(
        self, ws: websocket.WebSocketApp, close_status_code: str, close_msg: str
    ) -> None:
        self.debug(
            f"{self._classname} on_ws_close "
            f"(close_status_code={close_status_code}, close_msg={close_msg})"
        )

        if self.is_disposed:
            # do nothing
            pass

        elif self.is_disconnecting:
            self.debug(f"{self._classname} call soon closed.set_result(True)")
            self.closed.set_result(True)

        elif self.is_connecting or self.is_connected or self.is_ready:
            if self.can_reconnect:
                self._state = StreamCxnState.Reconnecting
                self._is_emit_reconnected = True
                if self.prepared.done():
                    self.prepared = Future()
                self._num_reconnect += 1
                self._config.set_next_url()
                delay_secs = delays.next()
                self.debug(
                    f"{self._classname} try to reconnect over url {self._config.url} "
                    f"in {delay_secs} secs, "
                    f"number of reconnections is {self._num_reconnect}"
                )
                self._timer.wait(delay_secs)
                self.connect()

            else:
                self._state = StreamCxnState.Disconnected
                self._emitter.emit(StreamCxnEvent.DISCONNECTED, self)
                self.dispose()

        else:
            debug_msg = (
                f"{self._classname} _on_ws_close: "
                f"don't know what to do, {self.state}"
            )
            if DEBUG:
                raise ValueError(debug_msg)

            else:
                self.error(debug_msg)

    def _on_ws_error(self, ws: websocket.WebSocketApp, exc: Exception) -> None:
        self.debug(f"{self._classname} on_ws_error")

        if DEBUG:
            self.debug(f"{traceback.format_exc()}")

        self.debug(f"{self._classname} Exception: {exc}")

    def _on_ws_ping(self, data: dict) -> None:
        self.debug(f"{self._classname} ping data={data}")

    def _on_ws_pong(self, ws, data: dict) -> None:
        self.debug(f"{self._classname} pong data={data}")

    def __str__(self) -> str:
        s = (
            f"{self.__class__.__name__} {{\n"
            f"\t\tname={self.name},\n"
            f"\t\tsubprotocol={self.subprotocol},\n"
            f"\t\tis_auto_reconnect={self._is_auto_reconnect},\n"
            f"\t\tmax_reconnect={self._max_reconnect},\n"
            f"\t\tcan_reconnect={self.can_reconnect}}}"
        )
        return s
