# coding: utf8

__all__ = ["Axis"]

from enum import Enum, unique

from ._common_tools import _convert_to_str, _normalize


@unique
class Axis(Enum):
    """
    The enumerate that specifies the unit for the axis.
    """

    X = "X"
    Y = "Y"
    Z = "Z"
    DATE = "Date"
    DELTA = "Delta"
    EXPIRY = "Expiry"
    MONEYNESS = "Moneyness"
    STRIKE = "Strike"
    TENOR = "Tenor"

    @staticmethod
    def convert_to_str(some):
        return _convert_to_str(Axis, _AXIS_VALUES, some)

    @staticmethod
    def normalize(some):
        return _normalize(_AXIS_VALUES_IN_LOWER_BY_AXIS, some)


_AXIS_VALUES = tuple(t.value for t in Axis)
_AXIS_VALUES_IN_LOWER_BY_AXIS = {
    name.lower(): item for name, item in Axis.__members__.items()
}
