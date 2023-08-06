from typing import List, Optional, TYPE_CHECKING, Union

from ._data_provider import DataProviderLayer, Response
from ._data_type import DataType
from ._endpoint_data import RequestMethod
from ..._core.session import get_valid_session
from ..._tools import validate_endpoint_request_url_parameters

if TYPE_CHECKING:
    from ..._core.session._session import Session
    from ._endpoint_data import RequestMethod
    from ._data_provider import Response


class Definition(DataProviderLayer):
    """
    This class defines a wrapper around the Data (request/response)
    delivery mechanism of the platform

    Parameters
    ----------
    url : str
        The Url presents the address of the endpoint
    method : RequestMethod, optional
        The RESTful Data service can support multiple methods
        when sending requests to a specified endpoint
    path_parameters : dict, optional
        Defines the path variables used to apply to the request
    query_parameters : dict, optional
        Defines the query variables used to apply to the request
    header_parameters : dict, optional
        Defines the header variables used to apply to the request
    body_parameters : dict, optional
        Defines the body variables used to apply to the request


    Examples
    --------
    >>> from refinitiv.data.delivery import endpoint_request
    >>> definition_endpoint = endpoint_request.Definition("/data/news/v1/analyze")
    """

    def __init__(
        self,
        url: str,
        method: "RequestMethod" = None,
        path_parameters: dict = None,
        query_parameters: dict = None,
        header_parameters: dict = None,
        body_parameters: Union[dict, List[dict]] = None,
    ):
        self.url = url
        self.method = method
        self.path_parameters = path_parameters
        self.query_parameters = query_parameters
        self.body_parameters = body_parameters
        self.header_parameters = header_parameters
        super().__init__(
            data_type=DataType.ENDPOINT,
            url=url,
            method=method,
            path_parameters=path_parameters,
            query_parameters=query_parameters,
            body_parameters=body_parameters,
            header_parameters=header_parameters,
        )

    def get_data(self, session: Optional["Session"] = None) -> "Response":
        """
        Returns a response from the API to the library

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data

        Returns
        -------
        Response

        Examples
        --------
        >>> from refinitiv.data.delivery import endpoint_request
        >>> definition_endpoint = endpoint_request.Definition("/data/news/v1/analyze")
        >>> definition_endpoint.get_data()
        """
        validate_endpoint_request_url_parameters(self.url, self.path_parameters)

        session = get_valid_session(session)
        response = self._provider.get_data(
            session,
            self.url,
            method=self.method,
            path_parameters=self.path_parameters,
            query_parameters=self.query_parameters,
            header_parameters=self.header_parameters,
            body_parameters=self.body_parameters,
        )
        return response

    async def get_data_async(self, session: Optional["Session"] = None) -> "Response":
        """
        Returns a response asynchronously from the API to the library

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data

        Returns
        -------
        Response

        Examples
        --------
        >>> from refinitiv.data.delivery import endpoint_request
        >>> definition_endpoint = endpoint_request.Definition("/data/news/v1/analyze")
        >>> await definition_endpoint.get_data_async()
        """
        validate_endpoint_request_url_parameters(self.url, self.path_parameters)

        session = get_valid_session(session)
        response = await self._provider.get_data_async(
            session,
            self.url,
            method=self.method,
            path_parameters=self.path_parameters,
            query_parameters=self.query_parameters,
            header_parameters=self.header_parameters,
            body_parameters=self.body_parameters,
        )
        return response
