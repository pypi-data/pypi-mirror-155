from datetime import date, datetime, timedelta
from typing import Optional, Union

from .._content_type import ContentType
from ..._tools import custom_insts_historical_universe_parser
from ...delivery._data._data_provider import DataProviderLayer


class Definition(DataProviderLayer):
    """
    Summary line of this class that defines parameters for requesting events from custom instruments

    Parameters
    ----------
    universe : str or list
        The Id or Symbol of custom instrument to operate on
    start : str or date or datetime or timedelta, optional
        The start date and timestamp of the query in ISO8601 with UTC only
    end : str or date or datetime or timedelta, optional
        The end date and timestamp of the query in ISO8601 with UTC only
    count : int, optional
        The maximum number of data returned. Values range: 1 - 10000

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments import events
    >>> definition_events = events.Definition("VOD.L")
    >>> response = definition_events.get_data()
    """

    def __init__(
        self,
        universe: Union[str, list],
        start: Optional[Union[str, date, datetime, timedelta]] = None,
        end: Optional[Union[str, date, datetime, timedelta]] = None,
        count: Optional[int] = None,
    ):
        universe = custom_insts_historical_universe_parser.get_list(universe)
        super().__init__(
            data_type=ContentType.CUSTOM_INSTRUMENTS_EVENTS,
            universe=universe,
            start=start,
            end=end,
            count=count,
        )
