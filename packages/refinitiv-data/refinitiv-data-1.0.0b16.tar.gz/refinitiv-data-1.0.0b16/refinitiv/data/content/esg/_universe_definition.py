from .._content_provider import ContentProviderLayer
from .._content_type import ContentType
from ..._tools import create_repr, validate_bool_value


class Definition(ContentProviderLayer):
    """
    This class describe parameters to retrieve data for ESG universe.

    Parameters
    ----------
    closure : str, optional
        Specifies the parameter that will be merged with the request

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    Examples
    --------
    >>> from refinitiv.data.content import esg
    >>> definition = esg.universe.Definition()
    >>> response = definition.get_data()

    >>> response = await definition.get_data_async()
    """

    def __init__(
        self,
        closure: str = None,
        use_field_names_in_headers: bool = False,
    ):
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            content_type=ContentType.ESG_UNIVERSE,
            closure=closure,
            use_field_names_in_headers=use_field_names_in_headers,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="universe",
            content=f"{{closure='{self._kwargs.get('closure')}'}}",
        )
