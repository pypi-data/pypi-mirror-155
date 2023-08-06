from typing import Optional

from .._content_type import ContentType
from ._data_provider_layer import (
    CustomInstrumentDataProviderLayer,
)


class Definition(CustomInstrumentDataProviderLayer):
    """
    Allows to create custom instrument, symbol and formula fields are mandatory, others are optional

    Parameters
    -----------
    universe : str
        The Id or Symbol of custom instrument to operate on. Use only for get_instrument().

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments import Definition
    >>> definition = Definition(universe="MyNewInstrument")
    >>> stream = definition.get_stream()
    """

    def __init__(
        self,
        universe: Optional[str],
    ):
        super().__init__(
            data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
            universe=universe,
        )
