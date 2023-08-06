from typing import Union, Optional, TYPE_CHECKING, Iterable

from ._symbol_type import SYMBOL_TYPE_VALUES
from ._symbology_provider_layer import SymbologyContentProviderLayer
from ..._tools import create_repr


if TYPE_CHECKING:
    from ._asset_class import AssetClass
    from ._country_code import CountryCode
    from ._asset_state import AssetState
    from ._symbol_type import SymbolTypes
    from .._types import ExtendedParams, OptStr, Strings


class Definition(SymbologyContentProviderLayer):
    """
    This class describe parameters to retrieve data for symbol conversion.

    Parameters
    ----------
    symbols: str or list of str
        Single instrument or list of instruments to convert.

    from_symbol_type: SymbolTypes, optional
        Instrument code to convert from.
        Possible values: 'CUSIP', 'ISIN', 'SEDOL', 'RIC', 'ticker', 'lipperID', 'IMO'
        Default: '_AllUnique'

    to_symbol_types: SymbolTypes, str or list of str or SymbolTypes, optional
        Instrument code to convert to.
        Possible values: 'CUSIP', 'ISIN', 'SEDOL', 'RIC', 'ticker', 'lipperID', 'IMO', 'OAPermID'
        Default: all symbol types are requested

    closure: str, optional
        Specifies the parameter that will be merged with the request

    extended_params: dict, optional
        Other parameters can be provided if necessary

    preferred_country_code: CountryCode, optional
        Unique ISO 3166 code for country

    asset_class: AssetClass, optional
        AssetClass value to build filter parameter.

    asset_state: AssetState, optional
        AssetState value to build filter parameter.

    Examples
    --------
    >>> from refinitiv.data.content import symbol_conversion
    >>> definition = symbol_conversion.Definition(
    >>>     symbols=["US5949181045", "US02079K1079"],
    >>>     from_symbol_type=symbol_conversion.SymbolTypes.ISIN,
    >>>     to_symbol_types=[symbol_conversion.SymbolTypes.RIC, symbol_conversion.SymbolTypes.OA_PERM_ID],
    >>>     preferred_country_code=symbol_conversion.CountryCode.USA,
    >>>     asset_class=[
    >>>        symbol_conversion.AssetClass.COMMODITIES,
    >>>        symbol_conversion.AssetClass.EQUITIES,
    >>>        symbol_conversion.AssetClass.WARRANTS
    >>>     ],
    >>>     asset_state=symbol_conversion.AssetState.INACTIVE)
    """

    def __init__(
        self,
        symbols: Union["Strings", str],
        from_symbol_type: Optional["SymbolTypes"] = "_AllUnique",
        to_symbol_types: Union[Iterable, str, "SymbolTypes"] = SYMBOL_TYPE_VALUES,
        closure: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
        preferred_country_code: Optional["CountryCode"] = None,
        asset_class: Union[Iterable, "AssetClass"] = None,
        asset_state: Optional["AssetState"] = None,
    ):
        self._symbols = symbols
        self._from_symbol_type = from_symbol_type
        self._to_symbol_types = to_symbol_types
        self._closure = closure
        self._extended_params = extended_params
        self.preferred_country_code = preferred_country_code
        self.asset_class = asset_class
        self.asset_state = asset_state

        super().__init__(
            symbols=self._symbols,
            from_symbol_type=self._from_symbol_type,
            to_symbol_types=self._to_symbol_types,
            closure=self._closure,
            extended_params=self._extended_params,
            preferred_country_code=self.preferred_country_code,
            asset_class=self.asset_class,
            asset_state=self.asset_state,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="content.symbols_convention",
            content=f"{{symbols='{self._symbols}'}}",
        )
