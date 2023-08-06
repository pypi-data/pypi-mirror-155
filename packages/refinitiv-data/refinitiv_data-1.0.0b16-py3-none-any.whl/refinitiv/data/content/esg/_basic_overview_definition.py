from typing import Iterable, Union

from .._content_provider import ContentProviderLayer
from .._content_type import ContentType
from ..._tools import create_repr, validate_bool_value


class Definition(ContentProviderLayer):
    """
    This class describe parameters to retrieve ESG basic data.

    Parameters
    ----------
    universe : str, list of str
        The Universe parameter allows the user to define the company they
        want content returned for, ESG content is delivered at the Company Level.

    closure : str, optional
        Specifies the parameter that will be merged with the request

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    Examples
    --------
    >>> from refinitiv.data.content import esg
    >>> definition = esg.basic_overview.Definition("IBM.N")
    >>> response = definition.get_data()

    >>> response = await definition.get_data_async()
    """

    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        closure: str = None,
        use_field_names_in_headers: bool = False,
    ):
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            content_type=ContentType.ESG_BASIC_OVERVIEW,
            universe=universe,
            closure=closure,
            use_field_names_in_headers=use_field_names_in_headers,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="basic_overview",
            content=f"{{universe='{self._kwargs.get('universe')}'}}",
        )
