from enum import Enum

from .._content_type import ContentType
from ..._tools import make_enum_arg_parser, ArgsParser, validate_bool_value


class DataGridType(Enum):
    UDF = "udf"
    RDP = "rdp"


data_grid_types_arg_parser = make_enum_arg_parser(DataGridType)
use_field_names_in_headers_arg_parser = ArgsParser(validate_bool_value)

data_grid_type_value_by_content_type = {
    DataGridType.UDF.value: ContentType.DATA_GRID_UDF,
    DataGridType.RDP.value: ContentType.DATA_GRID_RDP,
}
