from typing import Optional

from ._news_data_provider_layer import NewsDataProviderLayer
from ..._tools import create_repr

from .._content_type import ContentType


class Definition(NewsDataProviderLayer):
    """
    This class describes parameters to retrieve data for news story.

    Parameters
    ----------
    story_id : str
        News Story ID.

    closure : str, optional
        Specifies the parameter that will be merged with the request

    extended_params : dict, optional
        Other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import news
    >>> definition = news.story.Definition("urn:newsml:reuters.com:20201026:nPt6BSyBh")
    """

    def __init__(
        self,
        story_id: str,
        closure: Optional[str] = None,
    ):
        super().__init__(
            data_type=ContentType.NEWS_STORY_RDP,
            story_id=story_id,
            closure=closure,
        )
        self.story_id = story_id

    def __repr__(self):
        return create_repr(
            self,
            middle_path="story",
            content=f"{{story_id='{self.story_id}'}}",
        )
