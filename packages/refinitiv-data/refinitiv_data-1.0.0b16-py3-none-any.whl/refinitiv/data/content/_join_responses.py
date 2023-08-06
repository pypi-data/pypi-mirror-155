from types import SimpleNamespace
from typing import List, Callable, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame

from ..delivery._data._data_provider import Response, Data


def join_dfs(dfs: List[DataFrame], how: str = "inner") -> DataFrame:
    if len(dfs) == 0:
        raise ValueError(f"Cannot join dfs, because dfs list is empty, dfs={dfs}")

    df = dfs.pop()
    df = df.join(dfs, how=how)  # noqa
    df = df.convert_dtypes()

    return df


def join_responses(
    responses: List[Response],
    join_dataframes: Callable = pd.concat,
    response_class=Response,
    data_class=Data,
    reset_index=False,
) -> Response:
    def build_df(*args, **kwargs):
        dfs = []
        df = None

        for response in responses:
            dfs.append(response.data.df)

        all_dfs_is_none = all(a is None for a in dfs)
        if not all_dfs_is_none:
            df = join_dataframes(dfs)

        if reset_index and df is not None:
            df = df.reset_index(drop=True)

        return df

    if len(responses) == 1:
        return responses[0]

    raws = []
    http_statuses = []
    http_headers = []
    request_messages = []
    http_responses = []
    errors = []
    is_successes = []

    for response in responses:
        raws.append(response.data.raw)
        http_statuses.append(response.http_status)
        http_headers.append(response.http_headers)
        request_messages.append(response.request_message)
        http_responses.append(response.http_response)
        is_successes.append(response.is_success)

        if response.errors:
            errors += response.errors

    raw_response = SimpleNamespace()
    raw_response.headers = http_headers
    raw_response.request = request_messages
    is_success = any(is_successes)
    response = response_class(raw_response=raw_response, is_success=is_success)
    response.data = data_class(raws, dfbuilder=build_df)
    response.errors += errors
    response.http_response = http_responses
    response._status = http_statuses

    return response


def get_first_success_response(responses: List[Tuple[str, Response]]) -> Response:
    successful = (response for _, response in responses if response.is_success)
    first_successful = next(successful, None)
    return first_successful


def join_historical_responses(
    responses: List[Tuple[str, Response]],
    axis_name: str,
    fields: List[str],
) -> Response:
    if len(responses) == 1:
        inst_name, response = responses[0]

        if not response.is_success:
            return response

        def build_df(*args, **kwargs) -> DataFrame:
            df = data.df

            if fields:
                not_valid_columns = set(fields) - set(df.columns.values)
                df = df.assign(
                    **{column_name: pd.NA for column_name in not_valid_columns}
                )

            df.axes[1].name = inst_name
            df.index.name = axis_name
            return df

        data = response.data
        response.data = Data(response.data.raw, dfbuilder=build_df)
        return response

    def build_df_as_join_dfs(*args, **kwargs) -> DataFrame:
        response = get_first_success_response(responses)

        if not response:
            return DataFrame()

        df = response.data.df

        index = df.index.to_numpy()
        columns = (None,)

        dfs = []
        for inst_name, response in responses:
            df = response.data.df

            if fields and response.is_success:
                not_valid_columns = set(fields) - set(df.columns.values)
                df = df.assign(
                    **{column_name: np.NaN for column_name in not_valid_columns}
                )

            elif fields and df is None:
                df = DataFrame(columns=fields, index=index)

            elif df is None:
                df = DataFrame(columns=columns, index=index)

            df.columns = pd.MultiIndex.from_product([[inst_name], df.columns])
            dfs.append(df)

        df = join_dfs(dfs, how="outer")

        # when only one field
        if fields:
            _fields = fields
        else:
            _fields = list(dict.fromkeys([i[1] for i in df.columns]))
        if len(_fields) == 1:
            df.columns = [column[0] for column in df.columns]
            df.columns.name = _fields[0]

        if not df.empty:
            df = df.rename_axis(axis_name)
        return df

    raws = []
    errors = []
    http_statuses = []
    http_headers = []
    http_responses = []
    request_messages = []

    for inst_name, response in responses:
        raws.append(response.data.raw)
        http_statuses.append(response.http_status)
        http_headers.append(response.http_headers)
        request_messages.append(response.request_message)
        http_responses.append(response.http_response)

        if response.errors:
            errors += response.errors

    raw_response = SimpleNamespace()
    raw_response.request = request_messages
    raw_response.headers = http_headers
    response = Response(raw_response=raw_response, is_success=True)
    response.errors += errors
    response.data = Data(raws, dfbuilder=build_df_as_join_dfs)
    response._status = http_statuses
    response.http_response = http_responses

    return response
