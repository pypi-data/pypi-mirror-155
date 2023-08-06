import urllib

from pandas import DataFrame
from refinitiv.data._tools import urljoin

from ._data_types import BucketData, FileData, FileSetData, PackageData
from ._iter_object import IterObj
from ._tools import _get_query_params
from .._data._data_provider import (
    DataProvider,
    ResponseFactory,
    RequestFactory,
)


# --------------------------------------------------------------------------------------
#   Request factory
# --------------------------------------------------------------------------------------


class CFSRequestFactory(RequestFactory):
    def get_query_parameters(self, *_, **kwargs) -> list:
        return _get_query_params(**kwargs)

    def add_query_parameters(self, url, query_parameters) -> str:
        return "?".join([url, urllib.parse.urlencode(query_parameters, safe=";")])


class CFSPackageRequestFactory(CFSRequestFactory):
    def get_query_parameters(self, *_, **kwargs) -> list:
        package_id = kwargs.get("_package_id")
        if package_id is not None:
            return []

        return super().get_query_parameters(**kwargs)

    def get_url(self, *args, **kwargs):
        url = super().get_url(*args, **kwargs)
        url_id = kwargs.get("_package_id")
        if url_id is not None:
            url = urljoin(url, url_id)
        return url


class CFSStreamRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        return super().get_url(*args, **kwargs) + "/{id}/stream"

    def get_path_parameters(self, *_, **kwargs) -> dict:
        path_parameters = kwargs.get("path_parameters") or dict()
        file_id = kwargs.get("id")
        if file_id:
            path_parameters["id"] = file_id
        return path_parameters

    def get_query_parameters(self, *_, **kwargs) -> list:
        query_parameters = kwargs.get("query_parameters") or []
        query_parameters.append(("doNotRedirect", "true"))
        return query_parameters


# --------------------------------------------------------------------------------------
#   Response factory
# --------------------------------------------------------------------------------------


def cfs_build_df(raw, **kwargs):
    _value = raw.get("value") or [raw]
    _columns = set()
    for i in _value:
        _columns = _columns | i.keys()
    _columns = tuple(_columns)
    _data = [
        [value[key] if key in value else None for key in _columns] for value in _value
    ]
    _dataframe = DataFrame(_data, columns=_columns)
    return _dataframe


class CFSResponseFactory(ResponseFactory):
    def create_success(self, data, *args, **kwargs):
        session = args[0]
        inst = self.response_class(is_success=True, **data)
        dfbuilder = self.get_dfbuilder(kwargs)
        content_data = data.get("content_data")
        content_value = content_data.get("value") or [content_data]
        _iter_obj = IterObj(content_value, session, self.data_class)
        inst.data = self.data_class(content_data, _iter_obj, dfbuilder=dfbuilder)
        inst.data._owner = inst
        return inst

    def create_fail(self, data, *args, **kwargs):
        inst = self.response_class(is_success=False, **data)
        inst.data = self.data_class(data)
        inst.data._owner = inst
        return inst


# --------------------------------------------------------------------------------------
#   Data provider
# --------------------------------------------------------------------------------------


class CFSDataProvider(DataProvider):
    def __init__(self, data_class, request=CFSRequestFactory()):
        super().__init__(
            response=CFSResponseFactory(data_class=data_class),
            request=request,
        )


cfs_buckets_data_provider = CFSDataProvider(data_class=BucketData)
cfs_file_sets_data_provider = CFSDataProvider(data_class=FileSetData)
cfs_files_data_provider = CFSDataProvider(data_class=FileData)
cfs_packages_data_provider = CFSDataProvider(
    data_class=PackageData, request=CFSPackageRequestFactory()
)
cfs_stream_data_provider = DataProvider(request=CFSStreamRequestFactory())
