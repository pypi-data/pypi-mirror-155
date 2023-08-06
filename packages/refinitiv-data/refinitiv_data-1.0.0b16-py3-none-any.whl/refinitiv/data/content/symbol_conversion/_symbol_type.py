from enum import Enum, unique

from ._tools import _normalize


@unique
class SymbolTypes(Enum):
    """
    Symbol types to send in request, by default "RIC" is using.
    """

    RIC = "RIC"
    ISIN = "IssueISIN"
    CUSIP = "CUSIP"
    SEDOL = "SEDOL"
    TICKER_SYMBOL = "TickerSymbol"
    OA_PERM_ID = "IssuerOAPermID"
    LIPPER_ID = "FundClassLipperID"

    @staticmethod
    def convert_to_str(some):
        result = None
        if isinstance(some, str):
            if some in SYMBOL_TYPE_VALUES:
                result = some
            else:
                result = SymbolTypes.normalize(some)
        elif isinstance(some, SymbolTypes):
            result = some.value
        if result:
            return result
        else:
            raise AttributeError(f"Symbol type value must be in {SYMBOL_TYPE_VALUES}")

    @staticmethod
    def normalize(some: str) -> str:
        return _normalize(some, _SYMBOL_TYPE_VALUES_IN_LOWER_BY_SYMBOL_TYPE)


SYMBOL_TYPE_VALUES = tuple(t.value for t in SymbolTypes)
_SYMBOL_TYPE_VALUES_IN_LOWER_BY_SYMBOL_TYPE = {
    name.lower(): item for name, item in SymbolTypes.__members__.items()
}
