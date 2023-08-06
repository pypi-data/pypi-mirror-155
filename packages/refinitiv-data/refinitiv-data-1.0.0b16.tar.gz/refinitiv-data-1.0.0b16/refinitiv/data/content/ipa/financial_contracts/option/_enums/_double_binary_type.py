# coding: utf8

from enum import Enum, unique
from ...._enums._common_tools import (
    _convert_to_str,
    _normalize,
)


@unique
class DoubleBinaryType(Enum):
    DOUBLE_NO_TOUCH = "DoubleNoTouch"
    NONE = "None"

    @staticmethod
    def convert_to_str(some):
        return _convert_to_str(DoubleBinaryType, _DOUBLE_BINARY_TYPE_VALUES, some)

    @staticmethod
    def normalize(some):
        return _normalize(
            _DOUBLE_BINARY_TYPE_VALUES_IN_LOWER_BY_DOUBLE_BINARY_TYPE, some
        )


_DOUBLE_BINARY_TYPE_VALUES = tuple(t.value for t in DoubleBinaryType)
_DOUBLE_BINARY_TYPE_VALUES_IN_LOWER_BY_DOUBLE_BINARY_TYPE = {
    name.lower(): item for name, item in DoubleBinaryType.__members__.items()
}
