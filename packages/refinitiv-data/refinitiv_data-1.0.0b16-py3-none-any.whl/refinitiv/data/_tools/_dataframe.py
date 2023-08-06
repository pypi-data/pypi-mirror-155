import re
from typing import Iterable, Union, List

import pandas as pd
from pandas import DataFrame, MultiIndex
from pandas.core.tools.datetimes import DatetimeScalarOrArrayConvertible


def convert_df_columns_to_datetime(
    df: pd.DataFrame, pattern: str, utc: bool = None, delete_tz: bool = False
) -> pd.DataFrame:
    for i in df.columns:
        if pattern in i:
            df[i] = pd.to_datetime(df[i], utc=utc)

            if delete_tz:
                df[i] = df[i].dt.tz_localize(None)

    return df


def convert_df_columns_to_datetime_use_re_compile(
    df: pd.DataFrame, re_compile: re.compile
) -> pd.DataFrame:
    for column_name in df.columns:
        if re_compile.search(column_name):
            convert_column_df_to_datetime(df, column_name)

    return df


def convert_str_to_datetime(s: str) -> DatetimeScalarOrArrayConvertible:
    date = pd.to_datetime(s, utc=True)
    date = date.tz_localize(None)
    return date


def convert_column_df_to_datetime(
    df: pd.DataFrame, column_name: Union[int, str]
) -> pd.DataFrame:
    df[column_name] = pd.to_datetime(df[column_name], utc=True)
    df[column_name] = df[column_name].dt.tz_localize(None)

    return df


def convert_items_df_to_datetime(
    items: DatetimeScalarOrArrayConvertible,
) -> DatetimeScalarOrArrayConvertible:
    date_time_items = pd.to_datetime(items, utc=True)
    date_time_items = date_time_items.tz_localize(None)

    return date_time_items


def sort_df_by_universe(df: DataFrame, universe: List[str]) -> DataFrame:
    length = len(universe)

    if length == 1:
        return df

    columns = df.columns

    def make_getidx():
        get_index = universe.index
        if isinstance(columns, MultiIndex):

            def geti(i):
                return i[0]

        else:

            def geti(i):
                return i

        def inner(i):
            try:
                index = get_index(geti(i))
            except ValueError:
                index = length
            return index

        return inner

    getidx = make_getidx()
    # [3, 0, 2, 1]
    curr_order = [getidx(col) for col in columns]
    # [0, 1, 2, 3]
    expected_order = list(range(length))
    if curr_order != expected_order:
        sorted_columns = (col for _, col in sorted(zip(curr_order, columns)))
        df = df.reindex(columns=sorted_columns)
    return df
