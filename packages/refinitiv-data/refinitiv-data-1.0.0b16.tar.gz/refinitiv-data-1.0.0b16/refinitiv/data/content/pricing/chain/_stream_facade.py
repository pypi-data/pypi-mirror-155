import copy
from typing import Any, Callable, List, TYPE_CHECKING

from ._stream import StreamingChain
from ..._types import ExtendedParams, OptBool, OptInt, OptStr
from ...._core.session import get_valid_session
from ...._tools import cached_property, create_repr
from ....delivery._stream.base_stream import StreamOpenWithUpdatesMixin

if TYPE_CHECKING:
    from ...._core.session import Session


class Stream(StreamOpenWithUpdatesMixin):
    """
    Stream is designed to request streaming chains and decode it dynamically.
    This class also act like a cache for each part of the chain record.

    Parameters
    ----------
    name : str
        Single instrument name
    session : Session, optional
        The Session defines the source where you want to retrieve your data
    service : str, optional
        Name service
    skip_summary_links : bool, optional
        Store skip summary links
    skip_empty : bool, optional
        Store skip empty
    override_summary_links : int, optional
        Store the override number of summary links
    extended_params : dict, optional
        If necessary other parameters

    Methods
    -------
    open(**kwargs)
        Open the Stream connection

    close()
        Closes the Stream connection, releases resources

    is_chain
        True - stream was decoded as a chain
        False - stream wasn't identified as a chain

    Attributes
    __________
    constituents: list
        A list of constituents in the chain record or empty list

    """

    def __init__(
        self,
        name: str,
        session: "Session" = None,
        service: OptStr = None,
        skip_summary_links: OptBool = True,
        skip_empty: OptBool = True,
        override_summary_links: OptInt = None,
        extended_params: ExtendedParams = None,
    ) -> None:
        session = get_valid_session(session)
        self._name = name
        self._session = session
        self._service = service
        self._skip_summary_links = skip_summary_links
        self._skip_empty = skip_empty
        self._override_summary_links = override_summary_links
        self._extended_params = extended_params

    @cached_property
    def _stream(self) -> StreamingChain:
        streaming_chain = StreamingChain(
            name=self._name,
            session=self._session,
            service=self._service,
            skip_summary_links=self._skip_summary_links,
            skip_empty=self._skip_empty,
            override_summary_links=self._override_summary_links,
            extended_params=self._extended_params,
        )
        return streaming_chain

    @property
    def name(self) -> str:
        return self._stream.name

    @property
    def is_chain(self) -> bool:
        return self._stream.is_chain

    @property
    def num_summary_links(self) -> int:
        return self._stream.num_summary_links

    @property
    def summary_links(self) -> List[str]:
        return self._stream.summary_links

    @property
    def display_name(self) -> str:
        return self._stream.display_name

    @property
    def constituents(self) -> List[str]:
        return copy.deepcopy(self._stream.get_constituents())

    def on_add(self, func: Callable[[int, str, "Stream"], Any]) -> "Stream":
        func = make_callback(self, func)
        self._stream.on_add(func)
        return self

    def on_remove(self, func: Callable[[str, int, "Stream"], Any]) -> "Stream":
        func = make_callback(self, func)
        self._stream.on_remove(func)
        return self

    def on_update(self, func: Callable[[str, str, int, "Stream"], Any]) -> "Stream":
        func = make_callback(self, func)
        self._stream.on_update(func)
        return self

    def on_complete(self, func: Callable[[list, "Stream"], Any]) -> "Stream":
        func = make_callback(self, func)
        self._stream.on_complete(func)
        return self

    def on_error(self, func: Callable[[str, tuple, "Stream"], Any]) -> "Stream":
        func = make_error_callback(self, func)
        self._stream.on_error(func)
        return self

    def __repr__(self):
        return create_repr(
            self,
            content=f"{{name='{self._name}'}}",
            class_name=self.__class__.__name__,
        )


def make_callback(stream: Stream, func: Callable) -> Callable:
    """Return a callback functions with correct arguments order."""

    def callback(*args):
        func(*args, stream)

    return callback


def make_error_callback(stream: Stream, func: Callable) -> Callable:
    """Return a callback function with correct arguments order for error handling."""

    def callback(*args):
        args = reversed(args)
        func(*args, stream)

    return callback
