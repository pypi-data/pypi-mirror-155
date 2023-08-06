from typing import Any, Callable, TYPE_CHECKING

from ._quantitative_data_stream import QuantitativeDataStream
from ..._types import ExtendedParams
from ...._core.session import get_valid_session
from ...._tools import cached_property, create_repr, make_callback
from ....delivery._stream.base_stream import StreamOpenMixin

if TYPE_CHECKING:
    from pandas import DataFrame
    from ...._core.session import Session


class Stream(StreamOpenMixin):
    """
    Open a streaming quantitative analytic service subscription.

    Parameters
    ----------
    universe: dict

    fields: list

    extended_params: dict
        Default: None

    Methods
    -------
    open()
        Open the QuantitativeDataStream connection

    close()
        Close the QuantitativeDataStream connection, releases resources

    get_snapshot()
        Get DataFrame with stream

    """

    def __init__(
        self,
        universe: dict,
        fields: list = None,
        session: "Session" = None,
        extended_params: ExtendedParams = None,
    ) -> None:
        session = get_valid_session(session)
        self._universe = universe
        self._fields = fields
        self._session = session
        self._extended_params = extended_params

    @cached_property
    def _stream(self) -> QuantitativeDataStream:
        stream = QuantitativeDataStream(
            universe=self._universe,
            fields=self._fields,
            session=self._session,
            extended_params=self._extended_params,
        )
        return stream

    def get_snapshot(self) -> "DataFrame":
        """
        Returns DataFrame snapshot a streaming quantitative analytic service

        Returns
        -------
        pd.DataFrame
        """
        return self._stream.get_snapshot()

    def on_response(self, func: Callable[[list, list, "Stream"], Any]) -> "Stream":
        """
        This callback is called with the reference to the stream object,
        the instrument name and the instrument response

        Parameters
        ----------
        func : Callable
            Called when the stream has response

        Returns
        -------
        current instance
        """
        self._stream.on_response(make_fin_callback(func))
        return self

    def on_update(self, func: Callable[[list, list, "Stream"], Any]) -> "Stream":
        """
        This callback is called with the reference to the stream object,
        the instrument name and the instrument update

        Parameters
        ----------
        func : Callable
            Called when the stream has a new update

        Returns
        -------
        current instance
        """
        self._stream.on_update(make_fin_callback(func))
        return self

    def on_state(self, func: Callable[[list, "Stream"], Any]) -> "Stream":
        """
        This callback is called with the reference to the stream object,
        when the stream has new state

        Parameters
        ----------
        func : Callable
            Called when the stream has a new state

        Returns
        -------
        current instance
        """
        self._stream.on_alarm(make_callback(func))
        return self

    def __repr__(self):
        return create_repr(
            self,
            class_name=self.__class__.__name__,
        )


def make_fin_callback(func: Callable[["Stream", list, list], Any]) -> Callable:
    """Return a callback functions with correct arguments order."""

    def callback(stream, *args):
        func(*args, stream)

    return callback
