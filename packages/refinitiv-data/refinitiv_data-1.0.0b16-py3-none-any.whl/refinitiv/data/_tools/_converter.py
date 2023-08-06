import numpy as np
import pandas as pd


def convert_dict_to_df(data, columns) -> pd.DataFrame:
    if data:
        df = pd.DataFrame(np.array(data), columns=columns)
        if not df.empty:
            df.fillna(pd.NA, inplace=True)
            df = df.convert_dtypes()
    else:
        df = pd.DataFrame([], columns=columns)
    return df


def convert_content_data_to_df(
    content_data: dict, use_field_names_in_headers: bool = True
):
    if "headers" not in content_data or "data" not in content_data:
        return pd.DataFrame()

    if use_field_names_in_headers:
        key = "name"
    else:
        key = "title"

    headers_names = [header[key] for header in content_data["headers"]]
    return convert_dict_to_df(content_data["data"], headers_names)
