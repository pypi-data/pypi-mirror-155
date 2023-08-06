from enum import Enum, unique


@unique
class AssetState(Enum):
    """
    Asset state values for 'filter' parameter in request for SymbolConversion content object.
    """

    ACTIVE = "Active"
    INACTIVE = "Inactive"
