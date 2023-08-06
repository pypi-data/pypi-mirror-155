import re
import sys
from collections import Counter
from typing import Callable, Optional, Union, TYPE_CHECKING

import numpy as np
import pandas as pd
from pandas import DataFrame, Series, merge

from ._tools import get_name_columns_without_datetime
from .._core.session import get_default
from .._tools import (
    ADC_FUNC_PATTERN_IN_FIELDS,
    ADC_PARAM_IN_FIELDS,
    ADC_TR_PATTERN,
    DEBUG,
    fields_arg_parser,
    universe_arg_parser,
)
from .._tools._dataframe import convert_df_columns_to_datetime
from ..content import fundamental_and_reference
from ..content.pricing._stream_facade import Stream
from ..errors import RDError

NOT_ALLOWED_SNAPSHOT_FIELDS = {"Date"}


if TYPE_CHECKING:
    from logging import Logger


def get_data(
    universe: Union[str, list],
    fields: Union[str, list, None] = None,
    parameters: Union[str, dict, None] = None,
    use_field_names_in_headers: bool = False,
) -> DataFrame:
    """
    With this tool you can request data from ADC, realtime pricing data or
    combination of both;

    Parameters
    ----------
        universe: str | list ,
            instruments to request.
        fields: str | list .
            fields to request.
        parameters: str | dict,
            Single global parameter key=value or dictionary
            of global parameters to request.
        use_field_names_in_headers: bool
            Return field name as column headers for data instead of title


    Returns
    -------
    pandas.DataFrame

     Examples
    --------
    >>> get_data(universe=['IBM.N', 'VOD.L'], fields=['BID', 'ASK'])
    >>> get_data(
    ...     universe=['GOOG.O', 'AAPL.O'],
    ...     fields=['TR.EV','TR.EVToSales'],
    ...     parameters = {'SDate': '0CY', 'Curn': 'CAD'}
    ...)
    >>> get_data(
    ...     universe=['IBM.N', 'VOD.L'],
    ...     fields=['BID', 'ASK', 'TR.Revenue'],
    ...     parameters = {'SCale':6, 'SDate':0, 'EDate':-3, 'FRQ':'FY'}
    ...)
    """
    if isinstance(universe, str):
        universe = [universe]
    return _get_data(
        _fundamental_data=fundamental_and_reference.Definition,
        _pricing_stream=Stream(universe=universe, fields=fields),
        universe=universe,
        fields=fields,
        parameters=parameters,
        use_field_names_in_headers=use_field_names_in_headers,
    )


def _get_data(
    _fundamental_data: Callable, _pricing_stream: Stream, **kwargs
) -> DataFrame:
    universe = kwargs.pop("universe")
    logger = get_default().logger()
    fields = kwargs.pop("fields")
    use_field_names_in_headers = kwargs.pop("use_field_names_in_headers", False)

    adc_df = DataFrame()
    _add_flag(adc_df)

    pricing_df = DataFrame()
    _add_flag(pricing_df)

    fields = fields_arg_parser.get_list(fields) if fields else []
    parameters = kwargs.pop("parameters")

    adc_tr_fields = [i for i in fields if re.match(ADC_TR_PATTERN, i)]
    adc_funcs_in_fields = [i for i in fields if re.match(ADC_FUNC_PATTERN_IN_FIELDS, i)]

    adc_fields = adc_tr_fields + adc_funcs_in_fields

    pricing_fields = [
        i
        for i in fields
        if (i not in adc_fields) and (i not in NOT_ALLOWED_SNAPSHOT_FIELDS)
    ]

    is_parameters_in_adc = any(
        i for i in adc_fields if re.match(ADC_PARAM_IN_FIELDS, i)
    )
    is_parameters_requested = parameters or is_parameters_in_adc

    adc_default_df = _create_default_df(universe, adc_fields)

    # if adc_fields is empty, we need any field to get universe
    _fields = adc_fields or ["TR.RIC"]

    _adc_df = _send_request(
        data_provider=_fundamental_data,
        params={
            "universe": universe,
            "fields": _fields,
            "parameters": parameters,
            "use_field_names_in_headers": use_field_names_in_headers,
        },
        logger=logger,
        default_df=adc_default_df,
    )
    if adc_fields:
        adc_df = _adc_df

    # update universe
    universe = list(_adc_df.get("Instrument", universe))
    _pricing_stream._universe = universe
    _pricing_stream._stream._universe = universe
    _pricing_stream._stream.universe = universe_arg_parser.get_list(universe)

    if not adc_fields:
        _add_flag(adc_df, {"raise_exception": True, "exception": ""})

    if pricing_fields:
        pricing_default_df = _create_default_df(universe, pricing_fields)
        pricing_df = _get_snapshot(
            _pricing_stream, pricing_fields, logger, pricing_default_df
        )
    elif not fields:
        pricing_df = _get_snapshot(_pricing_stream, fields, logger, pricing_df)
    else:
        _add_flag(pricing_df, {"raise_exception": True, "exception": ""})

    _look_for_two_exceptions(pricing_df, adc_df)

    if pricing_df.empty:
        result = adc_df
    elif adc_df.empty:
        result = pricing_df
    elif is_parameters_requested and _both_flags_false(pricing_df, adc_df):
        result = _custom_merge(adc_df, pricing_df)
    else:
        try:
            result = merge(pricing_df, adc_df)
        except pd.errors.MergeError as e:
            logger.debug(
                f"pricing_df=\n"
                f"{pricing_df.to_string()}\n"
                f"adc_df=\n"
                f"{adc_df.to_string()}\n"
            )
            raise e

    columns = get_name_columns_without_datetime(result)
    result[columns] = result[columns].replace([pd.NaT, np.NaN], pd.NA)

    return result


def get_log_string(fields, universe):
    return f"Fields: {fields} for {universe}"


def _send_request(
    data_provider: Callable,
    params: dict,
    logger: "Logger",
    default_df: DataFrame = DataFrame(),
) -> DataFrame:
    fields = params.get("fields", "")
    universe = params["universe"]
    logger.info(f"Requesting {get_log_string(fields, universe)} \n")
    df = default_df

    try:
        response = data_provider(**params).get_data()
    except Exception as e:
        if DEBUG:
            raise e
        logger.exception(f"Failure sending request with {data_provider}")
        df.flags.exception_event = {
            "raise_exception": True,
            "exception": sys.exc_info()[:2],
        }
    else:
        request_messages = response.request_message
        statuses = response.http_status
        if not isinstance(response.request_message, list):
            request_messages = [response.request_message]
            statuses = [response.http_status]

        for request, status in zip(request_messages, statuses):
            path = request.url.path
            cur_universe = path.rsplit("/", 1)[-1]
            if cur_universe not in universe:
                cur_universe = universe
            logger.info(
                f"Request to {path} with {get_log_string(fields, cur_universe)}\n"
                f"status: {status}\n"
            )

        # this check can be removed after all API would return
        # dataframe in response or raise exception
        if response.data.df is not None:
            df = response.data.df
            df.flags.exception_event = {"raise_exception": False, "exception": None}
        else:
            df.flags.exception_event = {
                "raise_exception": True,
                "exception": response.http_status,
            }

    return df


def _rename_column_n_to_column(
    name: str, df: DataFrame, multiindex: bool = False, level: int = 1
) -> None:
    if multiindex:
        occurrences = (
            # fr"^{name}_\d+$" - searching columns like f"{name}_0", f"{name}_1"
            i
            for i in df.columns.levels[level]
            if re.match(rf"^{name}_\d+$", i)
        )
    else:
        occurrences = (i for i in df.columns if re.match(rf"^{name}_\d+$", i))

    df.rename(columns={i: name for i in occurrences}, inplace=True)


def _rename_column_to_column_n(name: str, df: DataFrame) -> None:
    new_names = []
    count = 0
    for i in df.columns:
        if i == name:
            if isinstance(i, tuple):
                column_name = i[1]
                column_name = f"{column_name}_{count}"
                i = (i[0], column_name)
            else:
                i = f"{i}_{count}"
            count += 1
        new_names.append(i)
    df.columns = new_names


def _custom_merge(df_1: DataFrame, df_2: DataFrame) -> DataFrame:
    date_column = "Date"
    instruments_column = "Instrument"

    if "instrument" in df_1:
        df_1.rename(columns={"instrument": instruments_column}, inplace=True)

    duplicated_columns = _find_and_rename_duplicated_columns(df_1)

    if date_column in duplicated_columns:
        date_column = f"{date_column}_0"

    convert_df_columns_to_datetime(df_1, pattern="Date", utc=True, delete_tz=True)

    if instruments_column in df_1 and date_column in df_1:
        grouped = df_1.groupby(instruments_column)
        latest_rows_indexes = grouped[date_column].idxmax(skipna=False)

    else:
        latest_rows_indexes = Series([])

    _remove_empty_rows(latest_rows_indexes)

    latest_info = df_1.loc[latest_rows_indexes]

    if not latest_info.empty:
        mediator = pd.merge(df_2, latest_info, how="outer")
        df_1 = df_1.replace({"": np.NaN})
        result = pd.merge(mediator, df_1, how="right")

    else:
        result = pd.merge(df_2, df_1, how="outer")

    for i in duplicated_columns:
        _rename_column_n_to_column(i, result)

    return result


def _get_snapshot(
    stream: Stream,
    fields: Optional[list],
    logger: "Logger",
    default_df: DataFrame = DataFrame(),
) -> Optional[DataFrame]:
    logger.info(f"Requesting pricing info for fields={fields} via websocket\n")
    df = default_df

    try:
        stream.open(with_updates=False)
        df = stream.get_snapshot(fields=fields)
        stream.close()
    except Exception:
        logger.exception(f"Failure retrieving snapshot for {stream._stream.universe}")
        df.flags.exception_event = {
            "raise_exception": True,
            "exception": sys.exc_info()[:2],
        }
    else:
        # detect if get_snapshot didn't return at least 1 field
        if df.shape[1] == 1:
            msg = f"No data in snapshot for {stream._stream.universe}"
            logger.exception(msg)
            df.flags.exception_event = {"raise_exception": True, "exception": msg}
        else:
            df.flags.exception_event = {"raise_exception": False, "exception": None}

    return df


def _find_and_rename_duplicated_columns(df: DataFrame) -> list:
    counted_columns = Counter(df.columns)
    duplicated_columns = [i for i, n in counted_columns.items() if n > 1]

    for i in duplicated_columns:
        _rename_column_to_column_n(i, df)

    return duplicated_columns


def _remove_empty_rows(series: Series) -> None:
    for name, value in series.items():
        if pd.isna(value):
            series.pop(name)


def _create_default_df(
    universe: list,
    fields: Optional[list] = None,
) -> DataFrame:
    df = DataFrame(
        {
            "Instrument": {n: i for n, i in enumerate(universe)},
            **{i: {} for i in fields},
        }
    )
    return df


def _look_for_two_exceptions(df_1: DataFrame, df_2: DataFrame) -> None:
    if (
        df_1.flags.exception_event["raise_exception"]
        and df_2.flags.exception_event["raise_exception"]
    ):
        ex1 = df_1.flags.exception_event["exception"]
        ex2 = df_2.flags.exception_event["exception"]

        raise RDError(1, f"\nNo data to return, please check errors:\n{ex1}\n{ex2}\n")


def _add_flag(df: DataFrame, flag: Optional[dict] = None) -> None:
    if flag is None:
        flag = {"raise_exception": False, "exception": ""}
    df.flags.exception_event = flag


def _both_flags_false(df_1: DataFrame, df_2: DataFrame) -> bool:
    return (
        not df_1.flags.exception_event["raise_exception"]
        and not df_2.flags.exception_event["raise_exception"]
    )
