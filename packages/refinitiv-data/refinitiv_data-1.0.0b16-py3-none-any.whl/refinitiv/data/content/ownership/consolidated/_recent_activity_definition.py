from typing import Iterable, Union, TYPE_CHECKING

from ..._content_provider import ContentProviderLayer
from ..._content_type import ContentType
from ...._tools import validate_bool_value

if TYPE_CHECKING:
    from ....content._types import ExtendedParams
    from .._enums import SortOrder


class Definition(ContentProviderLayer):
    """
    This class describe parameters to retrieve the latest 5 buy or sell activities for the requested company.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the companies for which the content is returned.

    sort_order: str, SortOrder
        The sortOrder parameter specifies ascending (asc) or descending (desc) Sort Order.

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import ownership
    >>> definition = ownership.consolidated.recent_activity.Definition("TRI.N", "asc")
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        sort_order: Union[str, "SortOrder"],
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            content_type=ContentType.OWNERSHIP_CONSOLIDATED_RECENT_ACTIVITY,
            universe=universe,
            sort_order=sort_order,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
