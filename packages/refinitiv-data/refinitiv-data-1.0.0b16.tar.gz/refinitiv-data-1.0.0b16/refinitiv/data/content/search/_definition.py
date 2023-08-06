# coding: utf-8

from ._search_view_type import SearchViews
from .._content_provider import ContentProviderLayer
from ..._tools import create_repr, validate_types


class Definition(ContentProviderLayer):
    """
    This class describe parameters to retrieve data for search.

    Parameters
    ----------
    query: str, optional
        Keyword argument for view

    view: SearchViews, optional
        The view for searching see at SearchViews enum.
        Default: SearchViews.SEARCH_ALL

    filter: str, optional
        Where query is for unstructured end-user-oriented restriction, filter is for
        structured programmatic restriction.

    order_by: str, optional
        Defines the order in which matching documents should be returned.

    boost: str, optional
        This argument supports exactly the same predicate expression syntax as filter,
        but where filter restricts which documents are matched at all,
        boost just applies a large scoring boost to documents it matches,
        which will almost always guarantee that they appear at the top of the results.

    select: str, optional
        A comma-separated list of the properties of a document to be returned in the response.

    top: int, optional
        the maximum number of documents to retrieve. Must be non-negative.
        default: 10

    skip: int, optional
        The number of documents to skip in the sorted result set before returning the
        next top.

    group_by: str, optional
        If specified, this must name a single Groupable property.
        returned documents are grouped into buckets based on their value for this
        property.

    group_count: str, optional
        When supplied in combination with group_by, sets the maximum number of documents
        to be returned per bucket.
        default: 3

    navigators: str, optional
        This can name one or more properties, separated by commas, each of which must
        be Navigable.

    extended_params : dict, optional
        other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import search
    >>> definition = search.Definition(query="cfo", view=search.SearchViews.PEOPLE)
    """

    def __init__(
        self,
        query: str = None,
        view: SearchViews = SearchViews.SEARCH_ALL,
        filter: str = None,
        order_by: str = None,
        boost: str = None,
        select: str = None,
        top: int = 10,
        skip: int = 0,
        group_by: str = None,
        group_count: int = 3,
        navigators: str = None,
        features: str = None,
        scope: str = None,
        terms: str = None,
        extended_params: dict = None,
    ):
        validate_types(group_count, [int], "group_count")
        validate_types(skip, [int], "skip")
        validate_types(top, [int], "top")

        self._query = query
        self._view = view
        self._boost = boost
        self._features = features
        self._filter = filter
        self._group_by = group_by
        self._group_count = group_count
        self._navigators = navigators
        self._order_by = order_by
        self._scope = scope
        self._select = select
        self._skip = skip
        self._terms = terms
        self._top = top
        self._extended_params = extended_params
        from .._content_type import ContentType

        super().__init__(
            content_type=ContentType.DISCOVERY_SEARCH,
            query=self._query,
            view=self._view,
            filter=self._filter,
            order_by=self._order_by,
            boost=self._boost,
            select=self._select,
            top=self._top,
            skip=self._skip,
            group_by=self._group_by,
            group_count=self._group_count,
            navigators=self._navigators,
            features=self._features,
            scope=self._scope,
            terms=self._terms,
            extended_params=self._extended_params,
        )

    def __repr__(self):
        return create_repr(self, content=f"{{query='{self._query}'}}")
