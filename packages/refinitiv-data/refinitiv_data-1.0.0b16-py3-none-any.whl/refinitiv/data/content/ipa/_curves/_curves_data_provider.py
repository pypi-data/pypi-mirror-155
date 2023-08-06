# coding: utf8
from typing import List, Callable

import numpy as np
import pandas as pd
from numpy import iterable

from ._models._curve import Curve, ForwardCurve, ZcCurve
from .._content_provider import CurvesAndSurfacesRequestFactory, get_type_by_axis
from ..._content_type import ContentType
from ...._tools._ipa_validate import do_all_elements_have_error
from ...._tools._dataframe import convert_df_columns_to_datetime
from ....delivery._data._data_provider import ContentValidator, ValidatorContainer
from ....delivery._data._data_provider import DataProvider, ResponseFactory, Data


# ---------------------------------------------------------------------------
#   ContentValidator
# ---------------------------------------------------------------------------


class CurvesContentValidator(ContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = True
        content_data = data.get("content_data")
        raw_curves = content_data.get("data")

        if not raw_curves:
            is_valid = False
            data["error_code"] = 1
            data["error_message"] = "Content data is None"

        elif isinstance(raw_curves, list):
            is_valid = not do_all_elements_have_error(data, raw_curves)

        return is_valid


# ---------------------------------------------------------------------------
#   Content data
# ---------------------------------------------------------------------------


def zc_curves_build_df(raw, **kwargs):
    """

    Parameters
    ----------
    raw : dict

    Returns
    -------
    DataFrame
    >>> raw
    ... {
    ...     "data": [
    ...         {
    ...             "curveTag": "TAG",
    ...             "error": {
    ...                 "id": "9fef13f4-6d11-4d71-a388-824ddcc8a95a/9fef13f4-6d11-4d71-a388-824ddcc8a95a",
    ...                 "code": "QPS-Curves.7",
    ...                 "message": "The service failed to find the curve definition",
    ...             },
    ...         },
    ...         {
    ...             "curveParameters": {
    ...                 "extrapolationMode": "None",
    ...                 "interpolationMode": "CubicDiscount",
    ...                 "interestCalculationMethod": "Dcb_Actual_Actual",
    ...                 "priceSide": "Mid",
    ...                 "calendarAdjustment": "Calendar",
    ...                 "calendars": ["EMU_FI"],
    ...                 "compoundingType": "Compounded",
    ...                 "useMultiDimensionalSolver": True,
    ...                 "useConvexityAdjustment": True,
    ...                 "useSteps": False,
    ...                 "convexityAdjustment": {
    ...                     "meanReversionPercent": 3.9012,
    ...                     "volatilityPercent": 0.863,
    ...                 },
    ...                 "valuationDate": "2022-02-09",
    ...             },
    ...             "curveDefinition": {
    ...                 "availableTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "availableDiscountingTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "currency": "EUR",
    ...                 "mainConstituentAssetClass": "Swap",
    ...                 "riskType": "InterestRate",
    ...                 "indexName": "EURIBOR",
    ...                 "source": "Refinitiv",
    ...                 "name": "EUR EURIBOR Swap ZC Curve",
    ...                 "id": "9d619112-9ab3-45c9-b83c-eb04cbec382e",
    ...                 "discountingTenor": "OIS",
    ...                 "ignoreExistingDefinition": False,
    ...                 "owner": "Refinitiv",
    ...                 "indexTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...             },
    ...             "curves": {
    ...                 "OIS": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.49456799906775206,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000135835178428,
    ...                             "ratePercent": -0.49456799906775206,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROSTR="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": True,
    ...                 },
    ...                 "1M": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000152780111917,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROND="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": False,
    ...                 },
    ...                 "3M": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000152780111917,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROND="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": False,
    ...                 },
    ...                 "6M": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000152780111917,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROND="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": False,
    ...                 },
    ...                 "1Y": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000152780111917,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROND="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": False,
    ...                 },
    ...             },
    ...         },
    ...     ]
    ... }
    """
    datas = raw.get("data", [])
    datas = datas or []
    dfs = []

    for data in datas:

        error = data.get("error")
        if error:
            continue

        curves = data.get("curves")
        for value in curves.values():
            curve_points = value.get("curvePoints")

            d = {}
            for curve_point in curve_points:
                for key, value in curve_point.items():
                    values = d.setdefault(key, [])
                    values.append(value)

            d.pop("instruments", None)

            df = pd.DataFrame(d)
            df = df.convert_dtypes()
            dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df = convert_df_columns_to_datetime(df, "Date", utc=True, delete_tz=True)
    return df


def forward_curve_build_df(raw, **kwargs):
    """

    Parameters
    ----------
    raw : dict

    Returns
    -------
    DataFrame

    Examples
    -------
    >>> raw
    ... {
    ...     "data": [
    ...         {
    ...             "error": {
    ...                 "id": "b6f9797d-72c8-4baa-84eb-6a079fc40ec5/b6f9797d-72c8-4baa-84eb-6a079fc40ec5",
    ...                 "code": "QPS-Curves.6",
    ...                 "message": "Invalid input: curveDefinition is missing",
    ...             }
    ...         },
    ...         {
    ...             "curveTag": "test_curve",
    ...             "curveParameters": {
    ...                 "interestCalculationMethod": "Dcb_Actual_Actual",
    ...                 "priceSide": "Mid",
    ...                 "calendarAdjustment": "Calendar",
    ...                 "calendars": ["EMU_FI"],
    ...                 "compoundingType": "Compounded",
    ...                 "useConvexityAdjustment": True,
    ...                 "useSteps": False,
    ...                 "valuationDate": "2022-02-09",
    ...             },
    ...             "curveDefinition": {
    ...                 "availableTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "availableDiscountingTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "currency": "EUR",
    ...                 "mainConstituentAssetClass": "Swap",
    ...                 "riskType": "InterestRate",
    ...                 "indexName": "EURIBOR",
    ...                 "source": "Refinitiv",
    ...                 "name": "EUR EURIBOR Swap ZC Curve",
    ...                 "id": "9d619112-9ab3-45c9-b83c-eb04cbec382e",
    ...                 "discountingTenor": "OIS",
    ...                 "ignoreExistingDefinition": False,
    ...                 "owner": "Refinitiv",
    ...             },
    ...             "forwardCurves": [
    ...                 {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2021-02-01",
    ...                             "startDate": "2021-02-01",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": 7.040811073443143,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2021-02-04",
    ...                             "startDate": "2021-02-01",
    ...                             "discountFactor": 0.999442450671571,
    ...                             "ratePercent": 7.040811073443143,
    ...                             "tenor": "1D",
    ...                         },
    ...                     ],
    ...                     "forwardCurveTag": "ForwardTag",
    ...                     "forwardStart": "2021-02-01",
    ...                     "indexTenor": "3M",
    ...                 }
    ...             ],
    ...         },
    ...     ]
    ... }
    """
    datas = raw.get("data", [])
    datas = datas or []
    dfs = []
    for data in datas:

        error = data.get("error")
        if error:
            continue

        forward_curves = data.get("forwardCurves")

        for forward_curve in forward_curves:
            curve_points = forward_curve.get("curvePoints")

            d = {}
            for curve_point in curve_points:
                for key, value in curve_point.items():
                    values = d.setdefault(key, [])
                    values.append(value)

            df = pd.DataFrame(d)
            df = df.convert_dtypes()
            dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df = convert_df_columns_to_datetime(df, "Date", utc=True, delete_tz=True)
    return df


def zc_curve_definitions_build_df(raw, **kwargs):
    data = raw.get("data", [])
    data = data or []
    curve_definitions = [d for d in data if d for d in d.get("curveDefinitions")]
    df = pd.DataFrame(curve_definitions)

    if not df.empty:
        df = df.convert_dtypes()
        df = convert_df_columns_to_datetime(df, "Date", utc=True, delete_tz=True)
    return df


class OneCurveData(Data):
    def __init__(self, raw, create_curves, dfbuilder):
        Data.__init__(self, raw, dfbuilder=dfbuilder)
        self._create_curves = create_curves
        self._curve = None

    @property
    def curve(self) -> Curve:
        if self._curve is None:
            curve = self._create_curves(self._raw)
            self._curve = curve[0]
        return self._curve


class CurvesData(Data):
    def __init__(self, raw, create_curves, dfbuilder):
        Data.__init__(self, raw, dfbuilder=dfbuilder)
        self._create_curves = create_curves
        self._curves = None

    @property
    def curves(self) -> List[Curve]:
        if self._curves is None:
            self._curves = self._create_curves(self._raw)
        return self._curves


def make_create_forward_curves(x_axis: str, y_axis: str) -> Callable:
    """
    Parameters
    ----------
    x_axis: str
        Name of key in curve point data for build X axis
    y_axis: str
        Name of key in curve point data for build Y axis

    Returns
    -------
    Callable
    """

    def create_forward_curves(raw: dict) -> list:
        """
        Curve point in "curvePoints":
        {
            "discountFactor": 1.0,
            "endDate": "2021-02-01",
            "ratePercent": -2.330761285491212,
            "startDate": "2021-02-01",
            "tenor": "0D"
        }
        Parameters
        ----------
        raw

        Returns
        -------
        list of ForwardCurve
        """
        curves = []
        for data in raw.get("data", []):
            for forward_curve in data.get("forwardCurves", []):
                x, y = [], []
                for point in forward_curve.get("curvePoints"):
                    end_date = point.get(x_axis)
                    x.append(end_date)
                    discount_factor = point.get(y_axis)
                    y.append(discount_factor)

                x = np.array(x, dtype=get_type_by_axis(x_axis))
                y = np.array(y, dtype=get_type_by_axis(y_axis))
                curve = ForwardCurve(x, y, **forward_curve)
                curves.append(curve)

        return curves

    return create_forward_curves


def make_create_zc_curves(x_axis: str, y_axis: str) -> Callable:
    """
    Parameters
    ----------
    x_axis: str
        Name of key in curve point data for build X axis
    y_axis: str
        Name of key in curve point data for build Y axis

    Returns
    -------
    Callable
    """

    def create_zc_curves(raw: dict) -> list:
        """
        Curve point in "curvePoints":
        {
            "discountFactor": 1.0,
            "endDate": "2021-07-27",
            "ratePercent": -0.7359148312458879,
            "startDate": "2021-07-27",
            "tenor": "ON",
            "instruments": [
                {
                    "instrumentCode": "SARON.S"
                }
            ]
        }
        Parameters
        ----------
        raw

        Returns
        -------
        list of ZcCurve
        """
        curves = []
        for data in raw.get("data", []):
            for index_tenor, zc_curve in data.get("curves", {}).items():
                x, y = [], []
                for point in zc_curve.get("curvePoints"):
                    end_date = point.get(x_axis)
                    x.append(end_date)
                    discount_factor = point.get(y_axis)
                    y.append(discount_factor)

                x = np.array(x, dtype=get_type_by_axis(x_axis))
                y = np.array(y, dtype=get_type_by_axis(y_axis))
                curve = ZcCurve(x, y, index_tenor, **zc_curve)
                curves.append(curve)

        return curves

    return create_zc_curves


curves_maker_by_content_type = {
    ContentType.FORWARD_CURVE: make_create_forward_curves(
        x_axis="endDate", y_axis="discountFactor"
    ),
    ContentType.ZC_CURVES: make_create_zc_curves(
        x_axis="endDate", y_axis="discountFactor"
    ),
}


def get_curves_maker(content_type):
    curves_maker = curves_maker_by_content_type.get(content_type)

    if not curves_maker:
        raise ValueError(f"Cannot find curves_maker for content_type={content_type}")

    return curves_maker


# ---------------------------------------------------------------------------
#   Response factory
# ---------------------------------------------------------------------------


class CurvesResponseFactory(ResponseFactory):
    def create_success(self, *args, **kwargs):
        data = args[0]
        raw = data.get("content_data")
        universe = kwargs.get("universe")
        inst = self.response_class(is_success=True, **data)
        dfbuilder = self.get_dfbuilder(kwargs)
        content_type = kwargs.get("__content_type__")

        if content_type is ContentType.ZC_CURVE_DEFINITIONS:
            data = Data(raw, dfbuilder=dfbuilder)

        else:
            curves_maker = get_curves_maker(content_type)
            if iterable(universe):
                data = CurvesData(raw, curves_maker, dfbuilder)

            else:
                data = OneCurveData(raw, curves_maker, dfbuilder)

        inst.data = data
        inst.data._owner = inst
        return inst


# ---------------------------------------------------------------------------
#   Data provider
# ---------------------------------------------------------------------------

curves_data_provider = DataProvider(
    request=CurvesAndSurfacesRequestFactory(),
    response=CurvesResponseFactory(),
    validator=ValidatorContainer(content_validator=CurvesContentValidator()),
)
