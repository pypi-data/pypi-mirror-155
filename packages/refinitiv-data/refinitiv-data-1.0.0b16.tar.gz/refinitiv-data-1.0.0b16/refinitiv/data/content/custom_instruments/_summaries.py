from datetime import date, datetime, timedelta
from typing import Optional, Union

from ._data_provider import get_content_type_by_interval
from .._intervals import DayIntervalType, get_day_interval_type, Intervals
from ..._tools import validate_types, custom_insts_historical_universe_parser
from ...delivery._data._data_provider import DataProviderLayer


class Definition(DataProviderLayer):
    """
    Summary line of this class that defines parameters for requesting summaries from custom instruments

    Parameters
    ----------
    universe : str or list
        The Id or Symbol of custom instrument to operate on
    interval : str or Intervals, optional
        The consolidation interval in ISO8601
    start : str or date or datetime or timedelta, optional
        The start date and timestamp of the query in ISO8601 with UTC only
    end : str or date or datetime or timedelta, optional
        The end date and timestamp of the query in ISO8601 with UTC only
    count : int, optional
        The maximum number of data returned. Values range: 1 - 10000

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments import summaries
    >>> definition_summaries = summaries.Definition("VOD.L")
    >>> response = definition_summaries.get_data()
    """

    def __init__(
        self,
        universe: Union[str, list],
        interval: Union[str, Intervals] = None,
        start: Optional[Union[str, date, datetime, timedelta]] = None,
        end: Optional[Union[str, date, datetime, timedelta]] = None,
        count: Optional[int] = None,
    ) -> None:
        day_interval_type = get_day_interval_type(interval or DayIntervalType.INTER)
        content_type = get_content_type_by_interval(day_interval_type)
        validate_types(count, [int, type(None)], "count")

        universe = custom_insts_historical_universe_parser.get_list(universe)

        super().__init__(
            data_type=content_type,
            day_interval_type=day_interval_type,
            universe=universe,
            interval=interval,
            start=start,
            end=end,
            count=count,
        )
