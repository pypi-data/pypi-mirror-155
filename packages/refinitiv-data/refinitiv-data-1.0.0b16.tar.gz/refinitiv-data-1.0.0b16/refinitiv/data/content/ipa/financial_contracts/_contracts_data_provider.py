from itertools import zip_longest
from typing import Any

import numpy
import pandas as pd
from pandas import DataFrame

from ._outputs import Outputs
from ..._content_provider import ErrorParser
from ...._tools import (
    ArgsParser,
    iterable,
    make_enum_arg_parser,
    fields_arg_parser,
)
from ...._tools._dataframe import convert_column_df_to_datetime
from ....delivery._data._data_provider import ContentValidator, ValidatorContainer
from ....delivery._data._data_provider import (
    RequestFactory,
    DataProvider,
    ResponseFactory,
    Data as ContentData,
)
from ....delivery.endpoint_request import RequestMethod


# --------------------------------------------------------------------------------------
#   Content data validator
# --------------------------------------------------------------------------------------


class ContractsContentValidator(ContentValidator):
    def validate(self, data, *args, **kwargs):
        content_data = data.get("content_data")
        status = content_data.get("status", "")

        if content_data is None:
            data["error_code"] = 1
            data["error_message"] = "Content data is None"
            return False

        elif status == "Error":
            data["error_code"] = content_data.get("code")
            data["error_message"] = content_data.get("message")
            return False

        else:
            return self._is_valid_if_have_all_errors(data, content_data)

    def _is_valid_if_have_all_errors(self, data: dict, content_data: dict) -> bool:
        headers = content_data.get("headers", [])
        datas = content_data.get("data", [])
        err_codes = []
        err_msgs = []

        for header, *data_items in zip(headers, *datas):
            header_name = header["name"]

            if "ErrorCode" == header_name:
                err_codes = data_items

            elif "ErrorMessage" == header_name:
                err_msgs = data_items

        counter = len(datas) or 1  # because datas can be empty list
        if err_codes or err_msgs:
            for err_code, err_msg in zip_longest(err_codes, err_msgs, fillvalue=None):
                if err_code or err_msg:
                    counter -= 1
                    error_codes = data.setdefault("error_code", [])
                    error_codes.append(err_code)
                    error_messages = data.setdefault("error_message", [])
                    error_messages.append(err_msg)

        if counter == 0:
            return False

        return True


# ---------------------------------------------------------------------------
#   Content data
# ---------------------------------------------------------------------------


def convert_data_items_to_datetime(df: pd.DataFrame, headers) -> pd.DataFrame:
    for index, header in enumerate(headers):
        header_type = header.get("type", "")
        if header_type == "DateTime" or header_type == "Date":
            convert_column_df_to_datetime(df, index)

    return df


def financial_contracts_build_df(raw: dict, **kwargs) -> pd.DataFrame:
    """
    Convert "data" from raw response bond to dataframe format
    """
    data = raw.get("data")
    headers = raw.get("headers")
    if data:
        numpy_array = numpy.array(data, dtype=object)
        df = DataFrame(numpy_array)
        df = convert_data_items_to_datetime(df, headers)
        df.columns = [header["name"] for header in headers]
        if not df.empty:
            df.fillna(pd.NA, inplace=True)
            df = df.convert_dtypes()
    else:
        df = DataFrame([], columns=[])
    return df


class Data(ContentData):
    """
    This class is designed for storing and managing the response instrument data
    """

    def __init__(self, raw, **kwargs):
        super().__init__(raw, **kwargs)
        self._analytics_headers = None
        self._analytics_data = None
        self._analytics_market_data = None
        self._analytics_statuses = None
        if raw:
            #   get headers
            self._analytics_headers = raw.get("headers")
            #   get data
            self._analytics_data = raw.get("data")
            #   get marketData
            self._analytics_market_data = raw.get("marketData")
            #   get statuses
            self._analytics_statuses = raw.get("statuses")

    @property
    def analytics_headers(self):
        return self._analytics_headers

    @property
    def analytics_data(self):
        return self._analytics_data

    @property
    def analytics_market_data(self):
        return self._analytics_market_data

    @property
    def analytics_statuses(self):
        return self._analytics_statuses

    @property
    def marketdata_df(self):
        """
        Convert "marketData" from raw response bond to dataframe format
        """
        return None


# ---------------------------------------------------------------------------
#   Request factory
# ---------------------------------------------------------------------------


class ContractsRequestFactory(RequestFactory):
    def get_request_method(self, *_, **kwargs):
        return kwargs.get("method", RequestMethod.POST)

    def get_body_parameters(self, *_, **kwargs):
        input_universe = kwargs.get("universe")
        input_universe = input_universe or kwargs.get("definition") or []

        if not isinstance(input_universe, list):
            input_universe = [input_universe]

        universe = []
        # convert universe's objects into json
        for i, item in enumerate(input_universe):
            # item can be a tuple (instrument, pricing_parameters)
            if iterable(item):
                data = get_data(*item)

            else:
                data = get_data(item)

            universe.append(data)

        body_parameters = {"universe": universe}

        fields = kwargs.get("fields") or []
        if fields:
            fields = fields_arg_parser.get_list(fields)
            body_parameters["fields"] = fields

        outputs = kwargs.get("outputs")
        if outputs:
            outputs = outputs_contracts_arg_parser.get_list(outputs)
            body_parameters["outputs"] = outputs

        pricing_parameters = kwargs.get("pricing_parameters")
        if pricing_parameters:
            body_parameters["pricingParameters"] = pricing_parameters.get_json()

        return body_parameters


def get_data(definition, pricing_parameters=None):
    fields = None
    if hasattr(definition, "_kwargs"):
        kwargs = getattr(definition, "_kwargs")
        definition = kwargs.get("definition")
        fields = kwargs.get("fields")
        pricing_parameters = kwargs.get("pricing_parameters")

    data = {
        "instrumentType": definition.get_instrument_type(),
        "instrumentDefinition": definition.get_json(),
    }

    if fields:
        fields = fields_arg_parser.get_list(fields)
        data["fields"] = fields

    if pricing_parameters:
        data["pricingParameters"] = pricing_parameters.get_json()

    return data


def process_universe_item(item, definition_class):
    # item can be empty string ""
    if item and isinstance(item, str):
        item = definition_class(item)

    elif isinstance(item, definition_class):
        return item

    else:
        raise ValueError(
            f"Invalid type of universe, expected str: {type(item)} is given"
        )

    return item


def process_universe(universe, definition_class, pricing_parameters_class=None):
    if iterable(universe):
        for i, item in enumerate(universe):

            if iterable(item):
                item, pricing_parameters = item

                if pricing_parameters_class and not isinstance(
                    pricing_parameters, pricing_parameters_class
                ):
                    raise ValueError(
                        f"Invalid type of pricing parameters, "
                        f"expected {pricing_parameters_class}: "
                        f"{type(pricing_parameters)} is given"
                    )

                item = process_universe_item(item, definition_class)
                item = (item, pricing_parameters)

            else:
                item = process_universe_item(item, definition_class)

            universe[i] = item

    else:
        universe = process_universe_item(universe, definition_class)

    return universe


def process_bond_instrument_code(code: Any) -> str:
    if code is None or isinstance(code, str):
        return code
    else:
        raise ValueError(
            f"Invalid type of instrument_code, string is expected."
            f"type: {type(code)} is given"
        )


universe_contracts_arg_parser = ArgsParser(process_universe)
outputs_contracts_arg_parser = make_enum_arg_parser(Outputs)
bond_instrument_code_arg_parser = ArgsParser(process_bond_instrument_code)

# ---------------------------------------------------------------------------
#   Data provider
# ---------------------------------------------------------------------------

contracts_data_provider = DataProvider(
    request=ContractsRequestFactory(),
    response=ResponseFactory(data_class=Data),
    validator=ValidatorContainer(content_validator=ContractsContentValidator()),
    parser=ErrorParser(),
)
