import re
from collections import Counter
from datetime import datetime, timedelta, date
from typing import Union, Optional, List, Iterable, Callable

import pandas as pd
from numpy import nan
from pandas import DataFrame, Index
from pandas import MultiIndex

from ._tools import get_name_columns_without_datetime
from .get_data import (
    ADC_TR_PATTERN,
    ADC_FUNC_PATTERN_IN_FIELDS,
    _find_and_rename_duplicated_columns,
    _rename_column_n_to_column,
)
from .get_data import _send_request
from .._core.session import get_default
from .._errors import RDError
from .._tools import ohlc, fr_datetime_adapter, DEBUG
from .._tools._dataframe import convert_df_columns_to_datetime
from ..content import fundamental_and_reference, custom_instruments
from ..content import historical_pricing
from ..content.historical_pricing._hp_data_provider import EventTypes

EVENTS_INTERVALS = ["tick", "tas", "taq"]

PRICING_PARAMS_NAMES = [
    "universe",
    "fields",
    "interval",
    "start",
    "end",
    "adjustments",
    "count",
    "eventTypes",
]
CUSTOM_INSTS_PARAMS_NAMES = ["universe", "start", "end", "count", "interval"]

INTERVALS = {
    "tick": {"event_types": None, "adc": "D"},
    "tas": {"event_types": EventTypes.TRADE, "adc": "D"},
    "taq": {"event_types": EventTypes.QUOTE, "adc": "D"},
    "minute": {"pricing": "PT1M", "adc": "D"},
    "1min": {"pricing": "PT1M", "adc": "D"},
    "5min": {"pricing": "PT5M", "adc": "D"},
    "10min": {"pricing": "PT10M", "adc": "D"},
    "30min": {"pricing": "PT30M", "adc": "D"},
    "60min": {"pricing": "PT60M", "adc": "D"},
    "hourly": {"pricing": "PT1H", "adc": "D"},
    "1h": {"pricing": "PT1H", "adc": "D"},
    "daily": {"pricing": "P1D", "adc": "D"},
    "1d": {"pricing": "P1D", "adc": "D"},
    "1D": {"pricing": "P1D", "adc": "D"},
    "7D": {"pricing": "P7D", "adc": "W"},
    "7d": {"pricing": "P7D", "adc": "W"},
    "weekly": {"pricing": "P1W", "adc": "W"},
    "1W": {"pricing": "P1W", "adc": "W"},
    "monthly": {"pricing": "P1M", "adc": "M"},
    "1M": {"pricing": "P1M", "adc": "M"},
    "quarterly": {"pricing": "P3M", "adc": "CQ"},
    "3M": {"pricing": "P3M", "adc": "CQ"},
    "6M": {"pricing": "P6M", "adc": "CS"},
    "yearly": {"pricing": "P1Y", "adc": "CY"},
    "1Y": {"pricing": "P1Y", "adc": "CY"},
}

NON_INTRA_DAY_INTERVALS = {
    "daily",
    "1d",
    "1D",
    "weekly",
    "7D",
    "7d",
    "1W",
    "monthly",
    "1M",
    "quarterly",
    "3M",
    "yearly",
    "1Y",
}


def get_history(
    universe: Union[str, list],
    fields: Union[str, list, None] = None,
    interval: Optional[str] = None,
    start: Union[str, date, datetime, timedelta] = None,
    end: Union[str, date, datetime, timedelta] = None,
    adjustments: Optional[str] = None,
    count: Optional[int] = None,
    use_field_names_in_headers: Optional[bool] = False,
) -> DataFrame:
    """
    With this tool you can request historical data from Pricing and ADC

    Parameters
    ----------
        universe: str | list
            instruments to request.
        fields: str | list, optional
            fields to request.
        interval: str, optional
            The consolidation interval. Supported intervals are:
            tick, tas, taq, minute, 1min, 5min, 10min, 30min, 60min, hourly, 1h, daily,
            1d, 1D, 7D, 7d, weekly, 1W, monthly, 1M, quarterly, 3M, 6M, yearly, 1Y
        start: str or date or datetime or timedelta, optional
            The start date and timestamp of the query in ISO8601 with UTC only
        end: str or date or datetime or timedelta, optional
            The end date and timestamp of the query in ISO8601 with UTC only
        adjustments : str, optional
            The adjustment
        count : int, optional
            The maximum number of data returned. Values range: 1 - 10000
        use_field_names_in_headers : bool, optional
            Return field name in headers instead of title

    Returns
    -------
    pandas.DataFrame

     Examples
    --------
    >>> get_history(universe="GOOG.O")
    >>> get_history(universe="GOOG.O", fields="tr.Revenue", interval="1Y")
    >>> get_history(
    ...     universe="GOOG.O",
    ...     fields=["BID", "ASK", "tr.Revenue"],
    ...     interval="1Y",
    ...     start="2015-01-01",
    ...     end="2020-10-01",
    ... )
    """
    if interval not in INTERVALS and interval is not None:
        raise ValueError(
            f"Not supported interval value.\nSupported intervals are:"
            f"{list(INTERVALS.keys())}"
        )

    _pricing_events = historical_pricing.events.Definition
    _pricing_summaries = historical_pricing.summaries.Definition
    _ci_events = custom_instruments.events.Definition
    _ci_summaries = custom_instruments.summaries.Definition
    _fundamental_data = fundamental_and_reference.Definition
    if isinstance(universe, str):
        universe = [universe]
    universe = list(dict.fromkeys(universe))
    if not fields:
        fields = []
    if isinstance(fields, str):
        fields = [fields]
    params = {
        "universe": universe,
        "fields": fields,
        "interval": interval,
        "start": start,
        "end": end,
        "adjustments": adjustments,
        "count": count,
        "use_field_names_in_headers": use_field_names_in_headers,
    }

    if interval in EVENTS_INTERVALS:
        p_provider = _pricing_events
        ci_provider = _ci_events
        params.pop("interval")
        params["eventTypes"] = INTERVALS[interval]["event_types"]
        index_name = "Timestamp"

    else:
        p_provider = _pricing_summaries
        ci_provider = _ci_summaries
        index_name = "Date"
    return _get_history(_fundamental_data, p_provider, ci_provider, params, index_name)


def _get_history(
    adc_provider: Callable,
    p_provider: Callable,
    ci_provider: Callable,
    params: dict,
    index_name: str,
) -> DataFrame:
    logger = get_default().logger()
    fields = params.get("fields")
    use_field_names_in_headers = params.get("use_field_names_in_headers")
    universe = params.get("universe")
    interval = params.get("interval")

    dfs = []
    duplicated_columns = []

    adc_params = get_adc_params(params)
    adc_and_pricing_universe = adc_params.get("universe")
    adc_fields = adc_params.get("fields")
    not_adc_fields = [i for i in fields if i not in adc_fields]
    universe_for_template = []

    if not adc_fields:
        adc_params["fields"] = ["TR.RIC"]

    # adc
    if adc_and_pricing_universe:
        _adc_df = _send_request(
            data_provider=adc_provider,
            params=adc_params,
            logger=logger,
        )
        DEBUG and logger.debug(f"DATAGRID --->\n{_adc_df.to_string()}\n")
        # update universe
        adc_and_pricing_universe = (
            get_universe_from_df(_adc_df) or adc_and_pricing_universe
        )
        universe_for_template.extend(adc_and_pricing_universe)
        if adc_fields:
            adc_df = _adc_df
            duplicated_columns = _find_and_rename_duplicated_columns(adc_df)
            if duplicated_columns:
                remove_duplicated_columns(adc_df, duplicated_columns)

            adc_df = to_multi_index(adc_df, adc_and_pricing_universe)
            dfs.append(adc_df)

        # pricing
        pricing_params = get_pricing_params(
            params, adc_and_pricing_universe, adc_fields
        )
        pricing_fields = pricing_params.get("fields")
        if not fields or pricing_fields:
            pricing_df = _send_request(
                data_provider=p_provider, params=pricing_params, logger=logger
            )
            pricing_df = to_multi_index(pricing_df, adc_and_pricing_universe)
            DEBUG and logger.debug(f"PRICING --->\n{pricing_df.to_string()}\n")
            if fields:
                _remove_fields_if_not_requested(
                    fields, use_field_names_in_headers, pricing_df
                )
            dfs.append(pricing_df)

    # custom_instruments
    ci_params = get_ci_params(params)
    ci_universe = ci_params.get("universe")
    if ci_universe:
        universe_for_template.extend(ci_universe)

        ci_df = _send_request(
            data_provider=ci_provider,
            params=ci_params,
            logger=logger,
        )
        DEBUG and logger.debug(f"CUSTOMINSTS --->\n{ci_df.to_string()}\n")
        ci_df = to_multi_index(ci_df, ci_universe)
        if fields:
            _remove_fields_if_not_requested(fields, use_field_names_in_headers, ci_df)

        dfs.append(ci_df)

    # join dfs
    _look_for_exceptions(dfs)
    universe_for_template.sort(
        key=lambda a: universe.index(a) if a in universe else float("inf")
    )
    df_template = get_df_template(
        universe_for_template, not_adc_fields, use_field_names_in_headers
    )

    result = join_dfs(dfs, df_template, universe, interval, index_name)
    for i in duplicated_columns:
        _rename_column_n_to_column(i, result, multiindex=True)

    result = _update_columns_title(result)
    result.ohlc = ohlc.__get__(result, None)

    return result


def remove_duplicated_columns(df, duplicated_columns):
    if df.index.name in {"Date", "date"}:
        date_column = df.index.name
    else:
        date_column = "Date"

    if date_column in duplicated_columns:
        date_column = f"{date_column}_0"

    convert_df_columns_to_datetime(df, pattern=date_column, utc=True, delete_tz=True)
    df.drop_duplicates(inplace=True)
    return df


def _remove_fields_if_not_requested(fields, use_field_names_in_headers, df):
    fields_list = fields
    if not use_field_names_in_headers:
        fields_list = [i[3:] if i.upper().startswith("TR.") else i for i in fields]

    fields_from_df = {i[1] for i in df.columns}
    for field in fields_from_df:
        field_not_in_fields_list = str(field).upper() not in {
            i.upper() for i in fields_list
        }
        if not df.empty and field_not_in_fields_list:
            df.drop(field, axis=1, level=1, inplace=True, errors="ignore")


def get_df_template(universe, fields, use_field_names_in_headers):
    if not universe or not fields:
        return DataFrame()

    if use_field_names_in_headers:
        fields_for_template = fields
    else:
        fields_for_template = [
            i[3:] if i.upper().startswith("TR.") else i for i in fields
        ]

    columns = pd.MultiIndex.from_tuples(
        [(name, field) for field in fields_for_template for name in universe]
    )
    df_template = DataFrame(columns=columns)
    return df_template


def join_dfs(dfs, df_template, universe, interval, index_name):
    result = dfs.pop(0)
    for df in dfs:
        result = result.join(df, how="outer")

    columns = get_name_columns_without_datetime(result)
    if not result.empty:
        result[columns] = result[columns].replace([pd.NaT, nan], pd.NA)
    result = pd.concat([df_template, result])

    result.sort_index(ascending=True, inplace=True)

    if isinstance(result.columns, MultiIndex):
        result = result.reindex(columns=sorted(result.columns))

    result = _sort_by_universe(result, universe)
    result.index.name = index_name
    result = _set_index_name_and_change_index_type(result, interval)
    return result


def filter_params_by_name(params: dict, names: Iterable[str]):
    result = {key: value for key, value in params.items() if key in names and value}
    return result


def get_ci_params(params):
    universe = params.get("universe", [])
    universe = [i for i in universe if i.startswith("S)")]
    custom_insts_params = filter_params_by_name(params, CUSTOM_INSTS_PARAMS_NAMES)
    custom_insts_params["universe"] = universe
    interval = custom_insts_params.get("interval")
    if interval is not None:
        custom_insts_params["interval"] = INTERVALS[custom_insts_params["interval"]][
            "pricing"
        ]
    return custom_insts_params


def get_pricing_params(params, universe, adc_fields):
    fields = params.get("fields")
    if fields:
        fields = [i for i in fields if i not in adc_fields]
    pricing_params = filter_params_by_name(params, PRICING_PARAMS_NAMES)
    interval = pricing_params.get("interval")
    if interval is not None:
        pricing_params["interval"] = INTERVALS[pricing_params["interval"]]["pricing"]
    pricing_params["universe"] = universe
    pricing_params["fields"] = fields
    return pricing_params


def get_adc_params(params: dict):
    fields = params.get("fields")
    _adc_params = _translate_pricing_params_to_adc(params)
    adc_fields = get_adc_fields(fields) if fields else []
    universe = params.get("universe", [])
    universe = [i for i in universe if not i.startswith("S)")]
    adc_params = {
        "universe": universe,
        "fields": adc_fields,
        "parameters": _adc_params,
        "row_headers": "date",
        "use_field_names_in_headers": params.get("use_field_names_in_headers"),
    }
    return adc_params


def get_universe_from_df(df):
    if "Instrument" in df:
        instrument = df["Instrument"]
        result = list(instrument)
    elif "RIC" in df:
        instrument = df["RIC"]
        result = list(instrument)
    else:
        columns = [column[0] for column in df.columns if isinstance(column, tuple)]
        result = list(dict.fromkeys(columns))
    return result


def get_adc_fields(fields):
    adc_tr_fields = [i for i in fields if re.match(ADC_TR_PATTERN, i)]
    adc_funcs_in_fields = [i for i in fields if re.match(ADC_FUNC_PATTERN_IN_FIELDS, i)]

    adc_fields = adc_tr_fields + adc_funcs_in_fields
    return adc_fields


def _look_for_exceptions(dfs: list):
    exceptions = []
    raise_exception = True
    for df in dfs:
        if (
            hasattr(df.flags, "exception_event")
            and df.flags.exception_event["raise_exception"]
        ):
            _exceptions = [
                i.message
                for i in df.flags.exception_event["exception"]
                if hasattr(i, "message")
            ]
            exceptions.extend(_exceptions)
        else:
            raise_exception = False
    if raise_exception:
        exceptions = "\n".join(exceptions)
        raise RDError(1, f"\nNo data to return, please check errors:\n {exceptions}")


def to_multi_index(df: DataFrame, universe: List[str]):
    _df = df
    if not isinstance(_df.columns, pd.MultiIndex):
        if len(universe) == 1:
            _df.columns = pd.MultiIndex.from_product([[universe[0]], _df.columns])
        elif _df.columns.name is not None:
            field = _df.columns.name
            _df.columns = pd.MultiIndex.from_tuples(
                [(_universe, field) for _universe in _df]
            )
        _df.columns.names = [None] * len(df.columns.names)
    return df


def _sort_by_universe(df: DataFrame, universe: List[str]) -> DataFrame:
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


def _update_columns_title(df: DataFrame) -> DataFrame:
    """
    Transform dataframe from:

                AAPL.O          IBM.N
                Revenue - Mean  Revenue - Mean
    Date
    2022-04-12  396147651250    <NA>
    2022-04-18  <NA>            60686514370

    to:

    Revenue - Mean  AAPL.O            IBM.N
    Date
    2022-04-12      396147651250      <NA>
    2022-04-18      <NA>              60686514370
    """

    columns = df.columns
    if isinstance(columns, MultiIndex):

        c_fields = Counter(col[1] for col in columns if len(col) == 2)
        c_universe = Counter(col[0] for col in columns if len(col) == 2)
        fields_keys = list(c_fields.keys())
        universe_keys = list(c_universe.keys())
        if len(universe_keys) == 1:
            df.columns = Index([col[1] for col in columns], name=universe_keys[0])
        elif len(fields_keys) == 1:
            df.columns = Index([col[0] for col in columns], name=fields_keys[0])

    return df


def _translate_pricing_params_to_adc(p_params: dict) -> dict:
    adc_params = {}

    start = p_params.get("start")
    if start is not None:
        adc_params["SDate"] = fr_datetime_adapter.get_str(start)

    end = p_params.get("end")
    if end is not None:
        adc_params["EDate"] = fr_datetime_adapter.get_str(end)

    interval = p_params.get("interval")
    if interval is not None:
        adc_params["FRQ"] = INTERVALS[interval]["adc"]

    return adc_params


def _set_index_name_and_change_index_type(df: DataFrame, interval):
    if interval is not None and interval not in NON_INTRA_DAY_INTERVALS:
        df.index.names = ["Timestamp"]

    if interval in NON_INTRA_DAY_INTERVALS or interval is None:

        if isinstance(df.index, pd.Index):
            df.index = pd.to_datetime(df.index)

        df.index = df.index.tz_localize(None)

    return df
