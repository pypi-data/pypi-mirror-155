from enum import unique, Enum


@unique
class OpenState(Enum):
    Opened = "Opened"
    Pending = "Pending"
    Closed = "Closed"
