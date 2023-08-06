from .._content_type import ContentType
from ...delivery._data._data_provider import DataProviderLayer


class Definition(DataProviderLayer):
    """
    This class describe parameters to retrieve data for search custom instrument

    Parameters
    ----------
    access : str
        The search based on relationship to the custom instrument, for now only "owner" is supported. Can be omitted, default value is "owner"

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments import search
    >>> definition_search = search.Definition("VOD.L")
    >>> response = definition_search.get_data()
    """

    def __init__(self, access: str = "owner"):
        super().__init__(data_type=ContentType.CUSTOM_INSTRUMENTS_SEARCH, access=access)
