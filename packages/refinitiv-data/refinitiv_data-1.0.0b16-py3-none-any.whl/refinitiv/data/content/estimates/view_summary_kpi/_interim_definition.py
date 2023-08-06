from typing import Iterable, Union, TYPE_CHECKING

from ..._content_provider import ContentProviderLayer
from ..._content_type import ContentType
from ...._tools import validate_bool_value

if TYPE_CHECKING:
    from ....content._types import OptBool, ExtendedParams


class Definition(ContentProviderLayer):
    """
    This class describe parameters to retrieves estimates summary values for KPI measures for interim periods.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the companies for which the content is returned.

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params: ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import estimates
    >>> definition = estimates.view_summary_kpi.interim.Definition(universe="BNPP.PA")
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        use_field_names_in_headers: "OptBool" = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            content_type=ContentType.ESTIMATES_VIEW_SUMMARY_KPI_INTERIM,
            universe=universe,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
