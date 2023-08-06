from datetime import timedelta, datetime, date
from typing import Union, Tuple, Callable, Optional

from ._news_data_provider_layer import NewsDataProviderLayer
from ._sort_order import SortOrder
from ..._tools import create_repr

from .._content_type import ContentType


class Definition(NewsDataProviderLayer):
    """
    This class describes parameters to retrieve data for news headlines.

    Parameters
    ----------
    query: str
        The user search query.

    count: int, optional
        Count to limit number of headlines. Min value is 0. Default: 10

    date_from: str or timedelta, optional
        Beginning of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.

    date_to: str or timedelta, optional
        End of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.

    sort_order: SortOrder
        Value from SortOrder enum. Default: SortOrder.new_to_old

    extended_params: dict, optional
        Other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import news
    >>> definition = news.headlines.Definition(
    ...     "Refinitiv",
    ...     date_from="20.03.2021",
    ...     date_to=timedelta(days=-4),
    ...     count=3
    ... )
    """

    def __init__(
        self,
        query: str,
        count: int = 10,
        date_from: Union[str, timedelta, Tuple[datetime, date]] = None,
        date_to: Union[str, timedelta, Tuple[datetime, date]] = None,
        sort_order: SortOrder = SortOrder.new_to_old,
        extended_params: dict = None,
    ):
        super().__init__(
            data_type=ContentType.NEWS_HEADLINES_RDP,
            query=query,
            count=count,
            date_from=date_from,
            date_to=date_to,
            sort_order=sort_order,
            extended_params=extended_params,
        )
        self._query = query

    def get_data(
        self,
        session=None,
        on_response=None,
        on_page_response: Optional[Callable] = None,
        closure: Optional[str] = None,
        **kwargs,
    ):
        """
        Returns a response from the API to the library

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data
        on_response : Callable, optional
            Callable object to process retrieved data
        on_page_response : Callable, optional
            Callable object to process retrieved data
        closure : str, optional
            Specifies the parameter that will be merged with the request

        Returns
        -------
        NewsHeadlinesResponse

        Raises
        ------
        AttributeError
            If user didn't set default session.

        Examples
        --------
        >>> from refinitiv.data.content import news
        >>> definition = news.headlines.Definition("Refinitiv",
        >>>                                        date_from="20.03.2021",
        >>>                                        date_to=timedelta(days=-4),
        >>>                                        count=3)
        >>> response = definition.get_data()
        """
        kwargs["on_page_response"] = on_page_response
        kwargs["closure"] = closure
        return super().get_data(session, on_response, **kwargs)

    async def get_data_async(
        self,
        session=None,
        on_response=None,
        on_page_response: Optional[Callable] = None,
        closure: Optional[str] = None,
        **kwargs,
    ):
        """
        Returns a response asynchronously from the API to the library

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data
        on_response : Callable, optional
            Callable object to process retrieved data
        on_page_response : Callable, optional
            Callable object to process retrieved data
        closure : str, optional
            Specifies the parameter that will be merged with the request

        Returns
        -------
        NewsHeadlinesResponse

        Raises
        ------
        AttributeError
            If user didn't set default session.

        Examples
        --------
        >>> from refinitiv.data.content import news
        >>> definition = news.headlines.Definition("Refinitiv",
        >>>                                        date_from="20.03.2021",
        >>>                                        date_to=timedelta(days=-4),
        >>>                                        count=3)
        >>> response = await definition.get_data_async()
        """
        kwargs["on_page_response"] = on_page_response
        kwargs["closure"] = closure
        return await super().get_data_async(session, on_response, **kwargs)

    def __repr__(self):
        return create_repr(
            self,
            middle_path="headlines",
            content=f"{{query='{self._query}'}}",
        )
