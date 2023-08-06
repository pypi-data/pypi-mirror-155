from typing import Union, Optional, TYPE_CHECKING

from .._ownership_data_provider import universe_ownership_arg_parser
from ..._content_provider import ContentProviderLayer
from ..._content_type import ContentType
from ...._tools import validate_types, validate_bool_value

if TYPE_CHECKING:
    from .._enums import Frequency
    from ....content._types import ExtendedParams

optional_date = Optional[Union[str, "datetime.datetime"]]


class Definition(ContentProviderLayer):
    """
    This class describe parameters to retrieve the fund shareholders investment information
    about the requested company, at the specified historical period.

    Parameters
    ----------
    universe: str
        The Universe parameter allows the user to define the single company for which the content is returned.

    frequency: str, Frequency
        The frequency parameter allows users to request the frequency of the time series data, either quarterly or monthly.
        Available values : M, Q

    start: str, datetime, optional
        The start parameter allows users to define the start date of a time series.
        Dates are to be defined either by absolute or relative syntax.
        Example, 20190529, -1Q, 1D, -3MA.

    end: str, datetime, optional
        The end parameter allows users to define the start date of a time series.
        Dates are to be defined either by absolute or relative syntax.
        Example, 20190529, -1Q, 1D, -3MA.

    limit: int, optional
        The limit parameter is used for paging. It allows users to select the number of records to be returned.

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import ownership
    >>> import datetime
    >>> definition = ownership.fund.shareholders_history_report.Definition("TRI.N", "M", start="-1Q")
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        universe: str,
        frequency: Union[str, "Frequency"],
        start: optional_date = None,
        end: optional_date = None,
        limit: Optional[int] = None,
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        universe = universe_ownership_arg_parser.parse(universe)
        validate_types(limit, [int, type(None)], "limit")
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            content_type=ContentType.OWNERSHIP_FUND_SHAREHOLDERS_HISTORY_REPORT,
            universe=universe,
            frequency=frequency,
            start=start,
            end=end,
            limit=limit,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
