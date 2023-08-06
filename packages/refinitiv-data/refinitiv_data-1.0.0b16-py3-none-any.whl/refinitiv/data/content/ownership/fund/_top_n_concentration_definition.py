from typing import Iterable, Union, TYPE_CHECKING

from ..._content_provider import ContentProviderLayer
from ..._content_type import ContentType
from ...._tools import validate_types, validate_bool_value

if TYPE_CHECKING:
    from ....content._types import ExtendedParams


class Definition(ContentProviderLayer):
    """
    This class describe parameters to retrieve the calculated concentration data
    by top 10, 20, 50, 100 fund investors.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the companies for which the content is returned.

    count: int
        Number of records

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import ownership
    >>> definition = ownership.fund.top_n_concentration.Definition("TRI.N", 30)
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        count: int,
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(count, [int], "count")
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            content_type=ContentType.OWNERSHIP_FUND_TOP_N_CONCENTRATION,
            universe=universe,
            count=count,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
