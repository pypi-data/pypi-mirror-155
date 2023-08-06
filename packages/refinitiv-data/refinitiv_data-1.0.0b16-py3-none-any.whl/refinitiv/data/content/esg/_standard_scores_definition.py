from typing import Iterable, Union

from ._base_definition import BaseDefinition
from .._content_type import ContentType
from ..._tools import validate_types, validate_bool_value


class Definition(BaseDefinition):
    """
    This class describe parameters to retrieve ESG standart scores data.

    Parameters
    ----------
    universe : str, list of str
        The Universe parameter allows the user to define the company they
        want content returned for, ESG content is delivered at the Company Level.

    start : int, optional
        Start & End parameter allows the user to request
         the number of Financial Years they would like returned.

    end : int, optional
        Start & End parameter allows the user to request
        the number of Financial Years they would like returned.

    closure : str, optional
        Specifies the parameter that will be merged with the request

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    Examples
    --------
    >>> from refinitiv.data.content import esg
    >>> definition = esg.standard_scores.Definition("6758.T")
    """

    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        start: int = None,
        end: int = None,
        closure: str = None,
        use_field_names_in_headers: bool = False,
    ):
        validate_types(start, [int, type(None)], "start")
        validate_types(end, [int, type(None)], "end")
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            content_type=ContentType.ESG_STANDARD_SCORES,
            universe=universe,
            start=start,
            end=end,
            closure=closure,
            use_field_names_in_headers=use_field_names_in_headers,
        )

    def __repr__(self):
        get_repr = super().__repr__()
        return get_repr.replace("esg", "esg.standard_scores")
