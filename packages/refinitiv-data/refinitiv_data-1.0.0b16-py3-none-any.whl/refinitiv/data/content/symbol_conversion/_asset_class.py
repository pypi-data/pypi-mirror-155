from enum import Enum, unique


@unique
class AssetClass(Enum):
    """
    Asset class values to build 'filter' parameter in request for SymbolConversion content object.
    """

    COMMODITIES = "Commodities"
    EQUITY_OR_INDEX_OPTIONS = "EquityOrIndexOptions"
    BOND_AND_STIR_FUTURES_AND_OPTIONS = "BondAndSTIRFuturesAndOptions"
    WARRANTS = "Warrants"
    EQUITIES = "Equities"
    INDICES = "Indices"
    EQUITY_INDEX_FUTURES = "EquityIndexFutures"
    FUNDS = "Funds"
    CERTIFICATES = "Certificates"
    BONDS = "Bonds"
    RESERVE_CONVERTIBLE = "ReverseConvertible"
    MINI_FUTURE = "MiniFuture"
    FX_AND_MONEY = "FXAndMoney"
