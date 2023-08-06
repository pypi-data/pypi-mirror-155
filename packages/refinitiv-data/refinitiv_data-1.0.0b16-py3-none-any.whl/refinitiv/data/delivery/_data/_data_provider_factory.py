from typing import TYPE_CHECKING, Any, Union

from ._api_type import APIType
from ._data_provider import DataProvider, default_data_provider
from ._data_type import DataType
from ._endpoint_data_provider import endpoint_data_provider
from ..cfs._cfs_data_provider import (
    cfs_buckets_data_provider,
    cfs_file_sets_data_provider,
    cfs_files_data_provider,
    cfs_packages_data_provider,
    cfs_stream_data_provider,
)
from ..._tools._common import urljoin
from ...content._content_type import ContentType
from ...content.custom_instruments._data_provider import (
    custom_instrument_data_provider,
    custom_instrument_search_data_provider,
    custom_instruments_events_data_provider,
    custom_instruments_interday_summaries_data_provider,
    custom_instruments_intraday_summaries_data_provider,
)
from ...content.esg._esg_data_provider import esg_data_provider
from ...content.estimates._data_provider import estimates_data_provider
from ...content.fundamental_and_reference._data_provider import (
    data_grid_rdp_data_provider,
    data_grid_udf_data_provider,
)
from ...content.historical_pricing._hp_data_provider import (
    hp_events_data_provider,
    hp_summaries_data_provider,
)
from ...content.ipa._curves._curves_data_provider import curves_data_provider
from ...content.ipa._surfaces._surfaces_data_provider import surfaces_data_provider
from ...content.ipa.financial_contracts._contracts_data_provider import (
    contracts_data_provider,
)
from ...content.news._news_data_provider import (
    news_headlines_data_provider_rdp,
    news_headlines_data_provider_udf,
    news_story_data_provider_rdp,
    news_story_data_provider_udf,
)
from ...content.ownership._ownership_data_provider import ownership_data_provider
from ...content.pricing._pricing_content_provider import pricing_data_provider
from ...content.pricing.chain._chains_data_provider import chains_data_provider
from ...content.search._data_provider import (
    search_data_provider,
    lookup_data_provider,
    metadata_data_provider,
)
from ...content.estimates._data_provider import estimates_data_provider
from ...content.pricing._pricing_content_provider import pricing_data_provider
from ...content.filings._data_provider import filings_data_provider
from ..._tools._common import urljoin

if TYPE_CHECKING:
    from ..._configure import _RDPConfig

data_provider_by_data_type = {
    ContentType.CHAINS: chains_data_provider,
    ContentType.CONTRACTS: contracts_data_provider,
    ContentType.CUSTOM_INSTRUMENTS_EVENTS: custom_instruments_events_data_provider,
    ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS: custom_instrument_data_provider,
    ContentType.CUSTOM_INSTRUMENTS_INTERDAY_SUMMARIES: custom_instruments_interday_summaries_data_provider,
    ContentType.CUSTOM_INSTRUMENTS_INTRADAY_SUMMARIES: custom_instruments_intraday_summaries_data_provider,
    ContentType.CUSTOM_INSTRUMENTS_SEARCH: custom_instrument_search_data_provider,
    ContentType.DATA_GRID_RDP: data_grid_rdp_data_provider,
    ContentType.DATA_GRID_UDF: data_grid_udf_data_provider,
    ContentType.DEFAULT: default_data_provider,
    ContentType.DISCOVERY_LOOKUP: lookup_data_provider,
    ContentType.DISCOVERY_METADATA: metadata_data_provider,
    ContentType.DISCOVERY_SEARCH: search_data_provider,
    ContentType.ESG_BASIC_OVERVIEW: esg_data_provider,
    ContentType.ESG_FULL_MEASURES: esg_data_provider,
    ContentType.ESG_FULL_SCORES: esg_data_provider,
    ContentType.ESG_STANDARD_MEASURES: esg_data_provider,
    ContentType.ESG_STANDARD_SCORES: esg_data_provider,
    ContentType.ESG_UNIVERSE: esg_data_provider,
    ContentType.ESTIMATES_VIEW_ACTUALS_ANNUAL: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_ACTUALS_INTERIM: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_ANNUAL: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_INTERIM: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_ANNUAL: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_NON_PERIODIC_MEASURES: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_ANNUAL: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_INTERIM: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_RECOMMENDATIONS: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_INTERIM: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_ANNUAL: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_HISTORICAL_SNAPSHOTS_KPI: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_INTERIM: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_NON_PERIODIC_MEASURES: estimates_data_provider,
    ContentType.ESTIMATES_VIEW_SUMMARY_RECOMMENDATIONS: estimates_data_provider,
    ContentType.FILINGS_RETRIEVAL: filings_data_provider,
    ContentType.FORWARD_CURVE: curves_data_provider,
    ContentType.HISTORICAL_PRICING_EVENTS: hp_events_data_provider,
    ContentType.HISTORICAL_PRICING_INTERDAY_SUMMARIES: hp_summaries_data_provider,
    ContentType.HISTORICAL_PRICING_INTRADAY_SUMMARIES: hp_summaries_data_provider,
    ContentType.NEWS_HEADLINES_RDP: news_headlines_data_provider_rdp,
    ContentType.NEWS_HEADLINES_UDF: news_headlines_data_provider_udf,
    ContentType.NEWS_STORY_RDP: news_story_data_provider_rdp,
    ContentType.NEWS_STORY_UDF: news_story_data_provider_udf,
    ContentType.OWNERSHIP_CONSOLIDATED_BREAKDOWN: ownership_data_provider,
    ContentType.OWNERSHIP_CONSOLIDATED_CONCENTRATION: ownership_data_provider,
    ContentType.OWNERSHIP_CONSOLIDATED_INVESTORS: ownership_data_provider,
    ContentType.OWNERSHIP_CONSOLIDATED_RECENT_ACTIVITY: ownership_data_provider,
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_HISTORY_REPORT: ownership_data_provider,
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_REPORT: ownership_data_provider,
    ContentType.OWNERSHIP_CONSOLIDATED_TOP_N_CONCENTRATION: ownership_data_provider,
    ContentType.OWNERSHIP_FUND_BREAKDOWN: ownership_data_provider,
    ContentType.OWNERSHIP_FUND_CONCENTRATION: ownership_data_provider,
    ContentType.OWNERSHIP_FUND_HOLDINGS: ownership_data_provider,
    ContentType.OWNERSHIP_FUND_INVESTORS: ownership_data_provider,
    ContentType.OWNERSHIP_FUND_RECENT_ACTIVITY: ownership_data_provider,
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_HISTORY_REPORT: ownership_data_provider,
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_REPORT: ownership_data_provider,
    ContentType.OWNERSHIP_FUND_TOP_N_CONCENTRATION: ownership_data_provider,
    ContentType.OWNERSHIP_INSIDER_SHAREHOLDERS_REPORT: ownership_data_provider,
    ContentType.OWNERSHIP_INSIDER_TRANSACTION_REPORT: ownership_data_provider,
    ContentType.OWNERSHIP_INVESTOR_HOLDINGS: ownership_data_provider,
    ContentType.OWNERSHIP_ORG_INFO: ownership_data_provider,
    ContentType.PRICING: pricing_data_provider,
    ContentType.SURFACES: surfaces_data_provider,
    ContentType.ZC_CURVE_DEFINITIONS: curves_data_provider,
    ContentType.ZC_CURVES: curves_data_provider,
    DataType.CFS_BUCKETS: cfs_buckets_data_provider,
    DataType.CFS_FILE_SETS: cfs_file_sets_data_provider,
    DataType.CFS_FILES: cfs_files_data_provider,
    DataType.CFS_PACKAGES: cfs_packages_data_provider,
    DataType.CFS_STREAM: cfs_stream_data_provider,
    DataType.ENDPOINT: endpoint_data_provider,
}

api_config_key_by_api_type = {
    APIType.CFS: "apis.file-store",
    APIType.CURVES_AND_SURFACES: "apis.data.quantitative-analytics-curves-and-surfaces",
    APIType.FINANCIAL_CONTRACTS: "apis.data.quantitative-analytics-financial-contracts",
    APIType.HISTORICAL_PRICING: "apis.data.historical-pricing",
    APIType.ESG: "apis.data.environmental-social-governance",
    APIType.PRICING: "apis.data.pricing",
    APIType.OWNERSHIP: "apis.data.ownership",
    APIType.CHAINS: "apis.data.pricing",
    APIType.DATA_GRID: "apis.data.datagrid",
    APIType.NEWS: "apis.data.news",
    APIType.DISCOVERY: "apis.discovery.search",
    APIType.ESTIMATES: "apis.data.estimates",
    APIType.CUSTOM_INSTRUMENTS: "apis.data.custom-instruments",
    APIType.FILINGS: "apis.data.filings",
}

api_type_by_data_type = {
    DataType.CFS_BUCKETS: APIType.CFS,
    DataType.CFS_FILE_SETS: APIType.CFS,
    DataType.CFS_FILES: APIType.CFS,
    DataType.CFS_PACKAGES: APIType.CFS,
    DataType.CFS_STREAM: APIType.CFS,
    ContentType.FORWARD_CURVE: APIType.CURVES_AND_SURFACES,
    ContentType.ZC_CURVES: APIType.CURVES_AND_SURFACES,
    ContentType.ZC_CURVE_DEFINITIONS: APIType.CURVES_AND_SURFACES,
    ContentType.SURFACES: APIType.CURVES_AND_SURFACES,
    ContentType.CONTRACTS: APIType.FINANCIAL_CONTRACTS,
    ContentType.HISTORICAL_PRICING_EVENTS: APIType.HISTORICAL_PRICING,
    ContentType.HISTORICAL_PRICING_INTERDAY_SUMMARIES: APIType.HISTORICAL_PRICING,
    ContentType.HISTORICAL_PRICING_INTRADAY_SUMMARIES: APIType.HISTORICAL_PRICING,
    ContentType.ESG_STANDARD_SCORES: APIType.ESG,
    ContentType.ESG_STANDARD_MEASURES: APIType.ESG,
    ContentType.ESG_FULL_MEASURES: APIType.ESG,
    ContentType.ESG_FULL_SCORES: APIType.ESG,
    ContentType.ESG_BASIC_OVERVIEW: APIType.ESG,
    ContentType.ESG_UNIVERSE: APIType.ESG,
    ContentType.PRICING: APIType.PRICING,
    ContentType.OWNERSHIP_CONSOLIDATED_BREAKDOWN: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_CONSOLIDATED_CONCENTRATION: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_CONSOLIDATED_INVESTORS: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_CONSOLIDATED_RECENT_ACTIVITY: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_HISTORY_REPORT: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_REPORT: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_CONSOLIDATED_TOP_N_CONCENTRATION: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_FUND_CONCENTRATION: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_FUND_BREAKDOWN: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_FUND_INVESTORS: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_FUND_RECENT_ACTIVITY: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_HISTORY_REPORT: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_REPORT: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_FUND_TOP_N_CONCENTRATION: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_FUND_HOLDINGS: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_INSIDER_SHAREHOLDERS_REPORT: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_INSIDER_TRANSACTION_REPORT: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_INVESTOR_HOLDINGS: APIType.OWNERSHIP,
    ContentType.OWNERSHIP_ORG_INFO: APIType.OWNERSHIP,
    ContentType.CHAINS: APIType.CHAINS,
    ContentType.DATA_GRID_RDP: APIType.DATA_GRID,
    ContentType.DATA_GRID_UDF: APIType.DATA_GRID,
    ContentType.NEWS_HEADLINES_RDP: APIType.NEWS,
    ContentType.NEWS_HEADLINES_UDF: APIType.NEWS,
    ContentType.NEWS_STORY_RDP: APIType.NEWS,
    ContentType.NEWS_STORY_UDF: APIType.NEWS,
    ContentType.DISCOVERY_SEARCH: APIType.DISCOVERY,
    ContentType.DISCOVERY_LOOKUP: APIType.DISCOVERY,
    ContentType.DISCOVERY_METADATA: APIType.DISCOVERY,
    ContentType.ESTIMATES_VIEW_ACTUALS_ANNUAL: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_ACTUALS_INTERIM: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_ANNUAL: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_INTERIM: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_ANNUAL: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_NON_PERIODIC_MEASURES: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_ANNUAL: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_INTERIM: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_RECOMMENDATIONS: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_INTERIM: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_NON_PERIODIC_MEASURES: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_RECOMMENDATIONS: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_ANNUAL: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_HISTORICAL_SNAPSHOTS_KPI: APIType.ESTIMATES,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_INTERIM: APIType.ESTIMATES,
    ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS: APIType.CUSTOM_INSTRUMENTS,
    ContentType.CUSTOM_INSTRUMENTS_SEARCH: APIType.CUSTOM_INSTRUMENTS,
    ContentType.CUSTOM_INSTRUMENTS_EVENTS: APIType.CUSTOM_INSTRUMENTS,
    ContentType.CUSTOM_INSTRUMENTS_INTRADAY_SUMMARIES: APIType.CUSTOM_INSTRUMENTS,
    ContentType.CUSTOM_INSTRUMENTS_INTERDAY_SUMMARIES: APIType.CUSTOM_INSTRUMENTS,
    ContentType.FILINGS_RETRIEVAL: APIType.FILINGS,
}

url_config_key_by_data_type = {
    DataType.CFS_BUCKETS: "endpoints.buckets",
    DataType.CFS_FILE_SETS: "endpoints.file-sets",
    DataType.CFS_FILES: "endpoints.files",
    DataType.CFS_PACKAGES: "endpoints.packages",
    DataType.CFS_STREAM: "endpoints.files",
    ContentType.FORWARD_CURVE: "endpoints.forward-curves",
    ContentType.ZC_CURVES: "endpoints.zc-curves",
    ContentType.ZC_CURVE_DEFINITIONS: "endpoints.zc-curve-definitions",
    ContentType.SURFACES: "endpoints.surfaces",
    ContentType.CONTRACTS: "endpoints.financial-contracts",
    ContentType.HISTORICAL_PRICING_EVENTS: "endpoints.events",
    ContentType.HISTORICAL_PRICING_INTERDAY_SUMMARIES: "endpoints.interday-summaries",
    ContentType.HISTORICAL_PRICING_INTRADAY_SUMMARIES: "endpoints.intraday-summaries",
    ContentType.ESG_STANDARD_SCORES: "endpoints.scores-standard",
    ContentType.ESG_STANDARD_MEASURES: "endpoints.measures-standard",
    ContentType.ESG_FULL_MEASURES: "endpoints.measures-full",
    ContentType.ESG_FULL_SCORES: "endpoints.scores-full",
    ContentType.ESG_BASIC_OVERVIEW: "endpoints.basic",
    ContentType.ESG_UNIVERSE: "endpoints.universe",
    ContentType.PRICING: "endpoints.snapshots",
    ContentType.OWNERSHIP_CONSOLIDATED_BREAKDOWN: "endpoints.consolidated.breakdown",
    ContentType.OWNERSHIP_CONSOLIDATED_CONCENTRATION: "endpoints.consolidated.concentration",
    ContentType.OWNERSHIP_CONSOLIDATED_INVESTORS: "endpoints.consolidated.investors",
    ContentType.OWNERSHIP_CONSOLIDATED_RECENT_ACTIVITY: "endpoints.consolidated.recent-activity",
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_HISTORY_REPORT: "endpoints.consolidated.shareholders-history-report",
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_REPORT: "endpoints.consolidated.shareholders-report",
    ContentType.OWNERSHIP_CONSOLIDATED_TOP_N_CONCENTRATION: "endpoints.consolidated.top-n-concentration",
    ContentType.OWNERSHIP_FUND_CONCENTRATION: "endpoints.fund.concentration",
    ContentType.OWNERSHIP_FUND_BREAKDOWN: "endpoints.fund.breakdown",
    ContentType.OWNERSHIP_FUND_INVESTORS: "endpoints.fund.investors",
    ContentType.OWNERSHIP_FUND_RECENT_ACTIVITY: "endpoints.fund.recent-activity",
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_HISTORY_REPORT: "endpoints.fund.shareholders-history-report",
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_REPORT: "endpoints.fund.shareholders-report",
    ContentType.OWNERSHIP_FUND_TOP_N_CONCENTRATION: "endpoints.fund.top-n-concentration",
    ContentType.OWNERSHIP_FUND_HOLDINGS: "endpoints.fund.holdings",
    ContentType.OWNERSHIP_INSIDER_SHAREHOLDERS_REPORT: "endpoints.insider.shareholders-report",
    ContentType.OWNERSHIP_INSIDER_TRANSACTION_REPORT: "endpoints.insider.transaction-report",
    ContentType.OWNERSHIP_INVESTOR_HOLDINGS: "endpoints.investor.holdings",
    ContentType.OWNERSHIP_ORG_INFO: "endpoints.org-info",
    ContentType.CHAINS: "endpoints.chains",
    ContentType.DATA_GRID_RDP: "endpoints.standard",
    ContentType.DATA_GRID_UDF: "endpoints.standard",
    ContentType.NEWS_HEADLINES_RDP: "endpoints.headlines",
    ContentType.NEWS_HEADLINES_UDF: "endpoints.headlines",
    ContentType.NEWS_STORY_RDP: "endpoints.stories",
    ContentType.NEWS_STORY_UDF: "endpoints.stories",
    ContentType.DISCOVERY_SEARCH: "endpoints.search",
    ContentType.DISCOVERY_LOOKUP: "endpoints.lookup",
    ContentType.DISCOVERY_METADATA: "endpoints.metadata",
    ContentType.ESTIMATES_VIEW_ACTUALS_ANNUAL: "endpoints.view-actuals.annual",
    ContentType.ESTIMATES_VIEW_ACTUALS_INTERIM: "endpoints.view-actuals.interim",
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_ANNUAL: "endpoints.view-actuals-kpi.annual",
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_INTERIM: "endpoints.view-actuals-kpi.interim",
    ContentType.ESTIMATES_VIEW_SUMMARY_ANNUAL: "endpoints.view-summary.annual",
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_NON_PERIODIC_MEASURES: "endpoints.view-summary.historical-snapshots-non-periodic-measures",
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_ANNUAL: "endpoints.view-summary.historical-snapshots-periodic-measures-annual",
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_INTERIM: "endpoints.view-summary.historical-snapshots-periodic-measures-interim",
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_RECOMMENDATIONS: "endpoints.view-summary.historical-snapshots-recommendations",
    ContentType.ESTIMATES_VIEW_SUMMARY_INTERIM: "endpoints.view-summary.interim",
    ContentType.ESTIMATES_VIEW_SUMMARY_NON_PERIODIC_MEASURES: "endpoints.view-summary.non-periodic-measures",
    ContentType.ESTIMATES_VIEW_SUMMARY_RECOMMENDATIONS: "endpoints.view-summary.recommendations",
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_ANNUAL: "endpoints.view-summary-kpi.annual",
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_HISTORICAL_SNAPSHOTS_KPI: "endpoints.view-summary-kpi.historical-snapshots-kpi",
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_INTERIM: "endpoints.view-summary-kpi.interim",
    ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS: "endpoints.instruments",
    ContentType.CUSTOM_INSTRUMENTS_SEARCH: "endpoints.search",
    ContentType.CUSTOM_INSTRUMENTS_EVENTS: "endpoints.events",
    ContentType.CUSTOM_INSTRUMENTS_INTERDAY_SUMMARIES: "endpoints.interday-summaries",
    ContentType.CUSTOM_INSTRUMENTS_INTRADAY_SUMMARIES: "endpoints.intraday-summaries",
    ContentType.FILINGS_RETRIEVAL: "endpoints.retrieval",
}


def _get_api_config_key(data_type: DataType) -> str:
    api_type = api_type_by_data_type.get(data_type)
    api_config_key = api_config_key_by_api_type.get(api_type)
    return api_config_key


def _get_url_config_key(data_type: DataType) -> str:
    return url_config_key_by_data_type.get(data_type)


def get_api_config(
    data_type: Union[DataType, ContentType], config: "_RDPConfig"
) -> Union[dict, Any]:
    api_config_key = _get_api_config_key(data_type)
    api_config = config.get(api_config_key)

    if api_config is None:
        raise AttributeError(
            f"Cannot find api_key, data_type={data_type} by key={api_config_key}"
        )

    return api_config


def get_base_url(data_type: DataType, config: "_RDPConfig") -> str:
    """
    Parameters
    ----------
    config: _RDPConfig
    data_type: DataType

    Returns
    -------
    string
    """
    api_config = get_api_config(data_type, config)
    base_url = api_config.get("url")
    return base_url


def get_url(
    data_type: Union[DataType, ContentType],
    config: "_RDPConfig",
    request_mode: str = None,
) -> str:
    """
    Parameters
    ----------
    config: _RDPConfig
    data_type: DataType
    request_mode: str in ["sync", "async"]

    Returns
    -------
    string
    """
    api_config = get_api_config(data_type, config)
    url_config_key = _get_url_config_key(data_type)

    if request_mode is None:
        request_mode = "sync"

    if request_mode not in ["sync", "async"]:
        raise AttributeError(f"Request mode not in ['sync', 'async'].")

    # Test if url_content is a json with sync/async endpoints
    url_config_key_with_request_mode = ".".join([url_config_key, request_mode])
    content_url = api_config.get(url_config_key_with_request_mode)

    if content_url is None:
        # then test if content_url is a single endpoint
        content_url = api_config.get(url_config_key)

    if content_url is None:
        raise AttributeError(
            f"Cannot find content_url, data_type={data_type} by key={url_config_key}"
        )

    base_url = api_config.get("url")
    url = urljoin(base_url, content_url)

    return url


def make_provider(data_type: Union[DataType, ContentType], **_) -> DataProvider:
    """
    Parameters
    ----------
    data_type: DataType

    Returns
    -------
    DataProvider
    """
    data_provider = data_provider_by_data_type.get(data_type)

    if data_provider is None:
        raise AttributeError(f"Cannot get data provider by content type: {data_type}")

    return data_provider
