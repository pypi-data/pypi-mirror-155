from typing import Callable, Any, Dict, Union

import pandas as pd

from ._content_type import ContentType
from ._df_build_type import DFBuildType
from ._df_builder import (
    dfbuilder_udf,
    dfbuilder_rdp,
    default_build_df,
    build_empty_df,
    historical_build_df,
)
from .custom_instruments._data_provider import (
    custom_instruments_intervals_build_df,
    custom_instruments_build_df,
)
from .ipa._curves._curves_data_provider import (
    forward_curve_build_df,
    zc_curve_definitions_build_df,
    zc_curves_build_df,
)
from .ipa.financial_contracts._contracts_data_provider import (
    financial_contracts_build_df,
)
from .news._tools import news_build_df_rdp, news_build_df_udf
from .pricing._pricing_content_provider import pricing_build_df
from .pricing.chain._chains_data_provider import chains_build_df
from .search._data_provider import (
    discovery_lookup_build_df,
    discovery_metadata_build_df,
    discovery_search_build_df,
)
from ..delivery._data._data_type import DataType
from ..delivery.cfs._cfs_data_provider import cfs_build_df

content_type_by_build_type: Dict[
    Union[ContentType, DataType], Callable[[Any, Dict[str, Any]], pd.DataFrame]
] = {
    ContentType.CHAINS: chains_build_df,
    ContentType.CONTRACTS: financial_contracts_build_df,
    ContentType.CUSTOM_INSTRUMENTS_EVENTS: historical_build_df,
    ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS: custom_instruments_build_df,
    ContentType.CUSTOM_INSTRUMENTS_INTERDAY_SUMMARIES: historical_build_df,
    ContentType.CUSTOM_INSTRUMENTS_INTRADAY_SUMMARIES: historical_build_df,
    ContentType.CUSTOM_INSTRUMENTS_SEARCH: custom_instruments_build_df,
    ContentType.DATA_GRID_RDP: {
        DFBuildType.INDEX: dfbuilder_rdp.build_index,
        DFBuildType.DATE_AS_INDEX: dfbuilder_rdp.build_date_as_index,
    },
    ContentType.DATA_GRID_UDF: {
        DFBuildType.INDEX: dfbuilder_udf.build_index,
        DFBuildType.DATE_AS_INDEX: dfbuilder_udf.build_date_as_index,
    },
    ContentType.DEFAULT: default_build_df,
    ContentType.DISCOVERY_LOOKUP: discovery_lookup_build_df,
    ContentType.DISCOVERY_METADATA: discovery_metadata_build_df,
    ContentType.DISCOVERY_SEARCH: discovery_search_build_df,
    ContentType.ESG_BASIC_OVERVIEW: dfbuilder_rdp.build_index,
    ContentType.ESG_FULL_MEASURES: dfbuilder_rdp.build_index,
    ContentType.ESG_FULL_SCORES: dfbuilder_rdp.build_index,
    ContentType.ESG_STANDARD_MEASURES: dfbuilder_rdp.build_index,
    ContentType.ESG_STANDARD_SCORES: dfbuilder_rdp.build_index,
    ContentType.ESG_UNIVERSE: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_ACTUALS_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_ACTUALS_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_NON_PERIODIC_MEASURES: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_RECOMMENDATIONS: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_HISTORICAL_SNAPSHOTS_KPI: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_NON_PERIODIC_MEASURES: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_RECOMMENDATIONS: dfbuilder_rdp.build_index,
    ContentType.FILINGS_RETRIEVAL: dfbuilder_rdp.build_index,
    ContentType.FORWARD_CURVE: forward_curve_build_df,
    ContentType.HISTORICAL_PRICING_EVENTS: historical_build_df,
    ContentType.HISTORICAL_PRICING_INTERDAY_SUMMARIES: historical_build_df,
    ContentType.HISTORICAL_PRICING_INTRADAY_SUMMARIES: historical_build_df,
    ContentType.NEWS_HEADLINES_RDP: news_build_df_rdp,
    ContentType.NEWS_HEADLINES_UDF: news_build_df_udf,
    ContentType.NEWS_STORY_RDP: build_empty_df,
    ContentType.NEWS_STORY_UDF: build_empty_df,
    ContentType.OWNERSHIP_CONSOLIDATED_BREAKDOWN: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_CONCENTRATION: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_INVESTORS: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_RECENT_ACTIVITY: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_HISTORY_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_TOP_N_CONCENTRATION: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_BREAKDOWN: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_CONCENTRATION: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_HOLDINGS: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_INVESTORS: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_RECENT_ACTIVITY: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_HISTORY_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_TOP_N_CONCENTRATION: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_INSIDER_SHAREHOLDERS_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_INSIDER_TRANSACTION_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_INVESTOR_HOLDINGS: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_ORG_INFO: dfbuilder_rdp.build_index,
    ContentType.PRICING: pricing_build_df,
    ContentType.SURFACES: default_build_df,
    ContentType.ZC_CURVE_DEFINITIONS: zc_curve_definitions_build_df,
    ContentType.ZC_CURVES: zc_curves_build_df,
    DataType.CFS_BUCKETS: cfs_build_df,
    DataType.CFS_FILE_SETS: cfs_build_df,
    DataType.CFS_FILES: cfs_build_df,
    DataType.CFS_PACKAGES: cfs_build_df,
    DataType.CFS_STREAM: default_build_df,
    DataType.ENDPOINT: default_build_df,
}


def get_dfbuilder(
    content_type: ContentType, dfbuild_type: DFBuildType = DFBuildType.INDEX
) -> Callable[[Any, Dict[str, Any]], pd.DataFrame]:
    builder_by_build_type = content_type_by_build_type.get(content_type)

    if not builder_by_build_type:
        raise ValueError(f"Cannot find mapping for content_type={content_type}")

    if hasattr(builder_by_build_type, "get"):
        builder = builder_by_build_type.get(dfbuild_type)

    else:
        builder = builder_by_build_type

    if not builder:
        raise ValueError(f"Cannot find mapping for dfbuild_type={dfbuild_type}")

    return builder
