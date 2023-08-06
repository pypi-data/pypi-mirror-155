import asyncio
import threading
from typing import List, Optional

import requests

from ..._open_state import OpenState
from ..._tools import DEBUG

codes = requests.codes

UNAUTHORIZED_CODES = {codes.bad, codes.unauthorized, codes.forbidden}


def is_open(session):
    return session.open_state is OpenState.Opened


def is_closed(session):
    return session.open_state is OpenState.Closed


def loop_exception_handler(loop, context):
    if DEBUG:
        raise context["exception"]


def handle_exception(task):
    exception = None

    try:
        exception = task.exception()
    except asyncio.CancelledError:
        pass

    if exception:
        raise exception


class NullResponse:
    text = ""
    status_code = 0

    def json(self):
        return {}


class Delays:
    def __init__(self, delays: List[int]) -> None:
        self._delays = delays
        self._index = 0

    def next(self) -> int:
        if self._index >= len(self._delays):
            self._index = len(self._delays) - 1
        delay = self._delays[self._index]
        self._index += 1
        return delay

    def reset(self):
        self._index = 0


SECONDS_5 = 5
SECONDS_10 = 10
SECONDS_15 = 15
MINUTE_1 = 60
MINUTES_5 = 5 * MINUTE_1
MINUTES_10 = 10 * MINUTE_1
MINUTES_15 = 15 * MINUTE_1
HOUR_1 = 60 * MINUTE_1
HOURS_2 = 2 * HOUR_1


def get_delays() -> Delays:
    delays = Delays(
        [
            SECONDS_5,
            SECONDS_10,
            SECONDS_15,
            MINUTES_5,
            MINUTES_15,
            HOUR_1,
            HOURS_2,
        ]
    )
    return delays


class Daemon(threading.Thread):
    def __init__(self, interval, name: Optional[str] = None) -> None:
        threading.Thread.__init__(self, name, daemon=True)
        self.finished = threading.Event()
        self.interval = interval

    def cancel(self):
        self.finished.set()

    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
