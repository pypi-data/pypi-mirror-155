from ._enums import Package
from .._content_provider import (
    UniverseContentValidator,
    ErrorParser,
)
from ..._tools import (
    universe_arg_parser,
    make_enum_arg_parser,
)
from ...delivery._data._data_provider import (
    DataProvider,
    RequestFactory,
    ValidatorContainer,
)


class EstimatesRequestFactory(RequestFactory):
    def get_query_parameters(self, *_, **kwargs) -> list:
        query_parameters = []
        universe = universe_arg_parser.get_str(kwargs.get("universe"), delim=",")
        query_parameters.append(("universe", universe))

        package = kwargs.get("package")
        if package is not None:
            package = package_estimates_arg_parser.get_str(package)
            query_parameters.append(("package", package))

        return query_parameters

    def extend_query_parameters(self, query_parameters, extended_params):
        # query_parameters -> [("param1", "val1"), ]
        result = dict(query_parameters)
        # result -> {"param1": "val1"}
        result.update(extended_params)
        # result -> {"param1": "val1", "extended_param": "value"}
        # return [("param1", "val1"), ("extended_param", "value")]
        return list(result.items())


package_estimates_arg_parser = make_enum_arg_parser(Package)

estimates_data_provider = DataProvider(
    request=EstimatesRequestFactory(),
    validator=ValidatorContainer(content_validator=UniverseContentValidator()),
    parser=ErrorParser(),
)
