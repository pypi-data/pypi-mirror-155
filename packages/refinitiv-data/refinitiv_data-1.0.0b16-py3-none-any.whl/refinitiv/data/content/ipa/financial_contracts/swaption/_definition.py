# coding: utf8

from typing import Optional, Iterable

from ._bermudan_swaption_definition import BermudanSwaptionDefinition
from ._swaption_definition import SwaptionInstrumentDefinition
from ._swaption_pricing_parameters import PricingParameters
from .. import swap
from .._base_definition import BaseDefinition
from ..._enums import BuySell, CallPut, ExerciseStyle, SwaptionSettlementType
from ....._tools import create_repr


class Definition(BaseDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_tag : str, optional
        User defined string to identify the instrument. It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported.
    end_date : str, optional
        Expiry date of the option.
    tenor : str, optional
        Tenor of the option.
    bermudan_swaption_definition : BermudanSwaptionDefinition, optional

    buy_sell : BuySell
        The direction of the trade in terms of the deal currency.
    call_put : CallPut
        Tells if the option is a call or a put.
    exercise_style : ExerciseStyle
        EURO or BERM or AMER.
    settlement_type : SwaptionSettlementType, optional
        The settlement type of the option if the option is exercised
    underlying_definition : swap.Definition
        The details of the underlying swap.
    strike_percent : float, optional
        Strike percent of the option expressed in % format.
    fields: list of str, optional
        Contains the list of Analytics that the quantitative analytic service will
        compute.
    pricing_parameters : PricingParameters, optional
        The pricing parameters to apply to this instrument. If pricing parameters
        are not provided at this level parameters defined globally at the request
        level are used. If no pricing parameters are provided globally default
        values apply.
    extended_params : dict, optional
        If necessary other parameters.

    Methods
    -------
    get_data(session=session, on_response=on_response, async_mode=None)
        Returns a response to the data platform
    get_data_async(session=session, on_response=on_response, async_mode=None)
        Returns a response to the async data platform
    get_stream(session=session, api="")
        Get stream quantitative analytic service subscription

    Examples
    --------
     >>> import refinitiv.data.content.ipa.financial_contracts as rdf
     >>> definition = rdf.swaption.Definition(
     ...   buy_sell=rdf.swaption.BuySell.BUY,
     ...   call_put=rdf.swaption.CallPut.CALL,
     ...   exercise_style=rdf.swaption.ExerciseStyle.BERM,
     ...   underlying_definition=rdf.swap.Definition(tenor="3Y", template="EUR_AB6E"),
     ...)
     >>> response = definition.get_data()

    Using get_stream
     >>> stream = definition.get_stream()
     >>> stream.open()
    """

    def __init__(
        self,
        *,
        instrument_tag: Optional[str] = None,
        end_date: Optional[str] = None,
        tenor: Optional[str] = None,
        bermudan_swaption_definition: Optional[BermudanSwaptionDefinition] = None,
        buy_sell: BuySell = None,
        call_put: CallPut = None,
        exercise_style: ExerciseStyle = None,
        settlement_type: Optional[SwaptionSettlementType] = None,
        underlying_definition: swap.Definition = None,
        strike_percent: Optional[float] = None,
        fields: Optional[Iterable[str]] = None,
        pricing_parameters: Optional[PricingParameters] = None,
        extended_params: Optional[dict] = None,
    ):
        self.underlying_definition = underlying_definition
        definition = SwaptionInstrumentDefinition(
            instrument_tag=instrument_tag,
            end_date=end_date,
            tenor=tenor,
            bermudan_swaption_definition=bermudan_swaption_definition,
            buy_sell=buy_sell,
            call_put=call_put,
            exercise_style=exercise_style,
            settlement_type=settlement_type,
            underlying_definition=underlying_definition,
            strike_percent=strike_percent,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="content.ipa.financial_contracts.swaption",
            content=f"{{underlying_definition='{self.underlying_definition}'}}",
        )
