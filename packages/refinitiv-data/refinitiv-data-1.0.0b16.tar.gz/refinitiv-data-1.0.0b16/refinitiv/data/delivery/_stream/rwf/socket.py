import json
import time
import logging
from typing import Callable, Optional

try:
    from ema import (
        OmmConsumer,
        OmmConsumerConfig,
        AppClient,
        CustomLoggerClient,
        LoggerSeverity,
        MapEntry,
    )  # noqa

    EMA_INSTALLED = True
except ImportError:
    EMA_INSTALLED = False
else:
    from .conversion import json_marketprice_msg_to_ema
    from .ema import (
        ema_login_message,
        create_programmatic_cfg,
        name_type_map,
        generate_login_msg,
    )


if EMA_INSTALLED:

    class EmaPythonLogger(CustomLoggerClient):
        def __init__(self):
            super().__init__(EmaPythonLogger.log)

        severity_logging_map: dict = {
            LoggerSeverity.NoLogMsg: 1000,  # higher than critical to avoid logging
            LoggerSeverity.Error: logging.ERROR,
            LoggerSeverity.Warning: logging.WARNING,
            LoggerSeverity.Success: logging.INFO,
            LoggerSeverity.Verbose: logging.DEBUG,
        }

        @staticmethod
        def log(callback_client_name: str, severity: LoggerSeverity, message: str):
            logging.log(
                EmaPythonLogger.severity_logging_map[severity],
                f"PythonLogger - {callback_client_name}: {message}",
            )


class RwfSocketApp:
    """Emulating WebsocketApp + WSAPI"""

    def __init__(
        self,
        host: str,
        port: int,
        on_open: Callable,
        on_msg: Callable,
        on_close: Callable,
        field_dict_path: Optional[str] = None,
        enumtype_path: Optional[str] = None,
        python_logger: bool = True,
    ):
        if not EMA_INSTALLED:
            raise ImportError("You need to install refinitiv-ema to use RwfSocketApp")

        self.host = host
        self.port = port

        self.field_dict_path = field_dict_path
        self.enumtype_path = enumtype_path
        self.on_open = on_open
        self.on_msg = on_msg
        self.on_close = on_close
        self.id = None
        self.handles = {}  # stream_id: handle
        self.consumer = None
        self.keep_running = False
        self._skip_login = True
        self._reissue_handle = None

        def refresh_msg_cb(msg, event):
            # TODO: Ema example has LoginRefresh and reissue timestamp inside,
            #  possibly useful?
            self._reissue_handle = event.get_handle()

        def msg_cb(msg, event):
            on_msg(self, f"[{msg.json()}]")

        def nothing_callback(msg, event):
            pass
            # logger.debug(f"login client message: {msg.json()}")

        self.client = AppClient(
            on_refresh_msg=msg_cb,
            on_update_msg=msg_cb,
            on_status_msg=msg_cb,
        )

        self.login_client = AppClient(
            on_refresh_msg=refresh_msg_cb,
            on_update_msg=nothing_callback,
            on_status_msg=nothing_callback,
        )
        if python_logger:
            self.ema_logger = EmaPythonLogger()
        else:
            self.ema_logger = None  # Will use internal OmmLoggerClient

    def close(self, **_):
        self.keep_running = False
        self.on_close(self, -100, "Just Closed")

    def run_forever(self, login_msg: dict):
        admin_msg = ema_login_message(**generate_login_msg(login_msg))
        pgcfg = create_programmatic_cfg(
            field_dict_path=self.field_dict_path,
            enumtype_path=self.enumtype_path,
            host=self.host,
            port=self.port,
        )
        config = OmmConsumerConfig().config(pgcfg).add_admin_msg(admin_msg)

        self.consumer: OmmConsumer = OmmConsumer(
            config, self.login_client, self.ema_logger
        )
        self.on_open(self)
        self.keep_running = True

        try:
            while self.keep_running:
                time.sleep(0.2)

        except (Exception, KeyboardInterrupt, SystemExit) as e:
            # self._callback(self.on_error, e)
            if isinstance(e, SystemExit):
                # propagate SystemExit further
                raise
            # teardown()
            return not isinstance(e, KeyboardInterrupt)

    def send(self, msg: str):
        msg = json.loads(msg)

        msg_type = msg.get("Type", "Request")
        msg_domain = msg.get("Domain", "MarketPrice")

        if msg_type == "Pong":
            # do nothing
            pass

        elif msg_type == "Request":  # open
            if msg_domain == "MarketPrice":
                ema_msg = json_marketprice_msg_to_ema(msg, self.consumer.field_id_map)
                handle = self.consumer.register_client(ema_msg, self.client)
                # TODO What if we have wrong message id?
                self.handles[msg["ID"]] = handle
                # logger.debug(f"new client registered for {msg['Key']['Name']}")
            elif msg_domain == "Login":
                if self._skip_login:
                    self._skip_login = False
                    # logger.debug("First login message sent during init, skipping...")
                elif self._reissue_handle is not None:
                    admin_msg = ema_login_message(**generate_login_msg(msg))
                    self.consumer.reissue(admin_msg, self._reissue_handle)
                else:
                    # do nothing
                    pass
                    # logger.error(
                    #     "Tried re-login, but has not received valid login "
                    #     "response beforehand."
                    # )

            else:
                raise ValueError(f"Unknown domain of Request message: {msg_domain}")

        elif msg_type == "Close":
            if msg_domain == "Login":
                self.close()  # TODO: is this right?
            else:
                # logger.debug("RwfSocket received Close message")
                self.consumer.unregister(self.handles[msg["ID"]])

        else:
            raise ValueError(f"Unknown message type: {msg_type}")
