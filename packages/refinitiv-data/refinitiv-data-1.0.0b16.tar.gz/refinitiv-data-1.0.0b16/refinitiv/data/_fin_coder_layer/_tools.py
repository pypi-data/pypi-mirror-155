from typing import List

import pandas as pd
from pandas.core.dtypes.common import is_datetime64_any_dtype


def get_name_columns_without_datetime(df: pd.DataFrame) -> List[str]:
    return [
        column_name
        for column_name, dtype in df.dtypes.to_dict().items()
        if not is_datetime64_any_dtype(dtype)
    ]
