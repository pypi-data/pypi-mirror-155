# coding: utf-8

from typing import TYPE_CHECKING

from .._content_provider import ContentProviderLayer
from ..._tools import create_repr

if TYPE_CHECKING:
    from ._search_view_type import SearchViews


class Definition(ContentProviderLayer):
    """
    This class describe parameters to retrieve data for search metadata.

    Parameters
    ----------

    view : SearchViews
        picks a subset of the data universe to search against. see SearchViews

    Examples
    --------
    >>> from refinitiv.data.content import search
    >>> definition = search.metadata.Definition(view=search.SearchViews.PEOPLE)
    """

    def __init__(self, view: "SearchViews"):
        self._view = view

        from .._content_type import ContentType

        super().__init__(
            content_type=ContentType.DISCOVERY_METADATA,
            view=self._view,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="metadata",
            content=f"{{view='{self._view}'}}",
        )
