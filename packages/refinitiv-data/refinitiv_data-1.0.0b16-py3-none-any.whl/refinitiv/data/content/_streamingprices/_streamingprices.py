# coding: utf8

import itertools
from concurrent.futures import ThreadPoolExecutor, wait
from typing import (
    Union,
    Callable,
    Iterable,
    TYPE_CHECKING,
    Tuple,
    ValuesView,
    KeysView,
    ItemsView,
    Dict,
)

import pandas as pd

from ._streamingprice import StreamingPrice
from .._types import Strings
from ..._core.session._default_session_manager import get_valid_session
from ..._tools import universe_arg_parser, fields_arg_parser, cached_property
from ...delivery._stream import (
    OMMStreamListener,
    StreamEvent,
    StreamStateManager,
    StreamStateEvent,
)
from ...delivery._stream.base_stream import StreamOpenWithUpdatesMixin
from ..._errors import ItemWasNotRequested

if TYPE_CHECKING:
    from ..._core.session._session import Session


def validate(name, input_values, requested_values):
    input_values = set(input_values)
    requested_values = set(requested_values)
    not_requested = input_values - requested_values
    has_not_requested = bool(not_requested)

    if has_not_requested:
        raise ItemWasNotRequested(name, not_requested, requested_values)


def get_available_fields(value_by_fields_by_inst_names):
    available_fields = set()
    for value_by_fields in value_by_fields_by_inst_names.values():
        fields = value_by_fields.keys()
        available_fields.update(fields)
    return available_fields


class PricingStream(StreamOpenWithUpdatesMixin):
    def __init__(self, stream: StreamingPrice):
        self._stream: StreamingPrice = stream

    @property
    def id(self) -> int:
        return self._stream.id

    @property
    def code(self):
        return self._stream.code

    @property
    def message(self):
        return self._stream.message

    @property
    def name(self):
        return self._stream.name

    @property
    def service(self):
        return self._stream.service

    @property
    def fields(self):
        return self._stream.fields

    @property
    def status(self):
        return self._stream.status

    @property
    def is_ok(self):
        return self._stream.is_ok

    def __enter__(self):
        return self._stream.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._stream.__exit__(exc_type, exc_val, exc_tb)

    def pause(self):
        return self._stream.pause()

    def resume(self):
        return self._stream.resume()

    def get_field_value(self, field):
        return self._stream.get_field_value(field)

    def get_fields(self, fields=None) -> dict:
        return self._stream.get_fields(fields)

    def keys(self):
        return self._stream.keys()

    def values(self):
        return self._stream.values()

    def items(self):
        return self._stream.items()

    def __iter__(self):
        return self._stream.__iter__()

    def __getitem__(self, field):
        return self._stream.__getitem__(field)

    def __len__(self):
        return self._stream.__len__()

    def __repr__(self):
        return self._stream.__repr__()

    def __str__(self):
        return self._stream.__str__()


_id_iterator = itertools.count()


class StreamingPrices(StreamStateManager, OMMStreamListener["StreamingPrices"]):
    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        session: "Session" = None,
        fields: Union[str, list] = None,
        service: str = None,
        on_refresh: Callable = None,
        on_status: Callable = None,
        on_update: Callable = None,
        on_complete: Callable = None,
        extended_params: dict = None,
    ) -> None:
        session = get_valid_session(session)

        StreamStateManager.__init__(self, logger=session.logger())
        OMMStreamListener.__init__(
            self,
            logger=session.logger(),
            on_refresh=on_refresh,
            on_status=on_status,
            on_update=on_update,
            on_complete=on_complete,
        )

        self.universe: Strings = universe_arg_parser.get_list(universe)
        self._session = session
        self.fields: Strings = fields_arg_parser.get_list(fields or [])
        self._service = service
        self._extended_params = extended_params
        self._id = next(_id_iterator)
        self._classname: str = (
            f"[{self.__class__.__name__} id={self._id} universe={universe}]"
        )
        self._completed = set()

    @cached_property
    def _streaming_prices_by_name(self) -> Dict[str, StreamingPrice]:
        retval = {}
        for name in self.universe:
            streaming_price = StreamingPrice(
                session=self._session,
                name=name,
                fields=self.fields,
                service=self._service,
                on_refresh=self._on_stream_refresh,
                on_status=self._on_stream_status,
                on_update=self._on_stream_update,
                on_complete=self._on_stream_complete,
                on_error=self._on_stream_error,
                extended_params=self._extended_params,
                parent_id=self._id,
            )

            streaming_price.on(StreamStateEvent.CLOSED, self._on_stream_close)
            retval[name] = streaming_price
        return retval

    def keys(self) -> KeysView[str]:
        return self._streaming_prices_by_name.keys()

    def values(self) -> ValuesView[StreamingPrice]:
        return self._streaming_prices_by_name.values()

    def items(self) -> ItemsView[str, StreamingPrice]:
        return self._streaming_prices_by_name.items()

    def __iter__(self):
        return StreamingPricesIterator(self)

    def __getitem__(self, name) -> PricingStream:
        streaming_price = self._streaming_prices_by_name.get(name, {})

        if streaming_price == {}:
            self._warning(f"'{name}' not in {self._classname} universe")
            return streaming_price

        if hasattr(streaming_price, "_wrapper"):
            wrapper = streaming_price._wrapper
        else:
            wrapper = PricingStream(streaming_price)
            streaming_price._wrapper = wrapper

        return wrapper

    def __len__(self):
        return len(self._streaming_prices_by_name)

    def get_snapshot(
        self, universe: Strings = None, fields: Strings = None, convert: bool = True
    ) -> pd.DataFrame:
        """
        Returns a Dataframe filled with snapshot values
        for a list of instrument names and a list of fields.

        Parameters
        ----------
        universe: list of strings
            List of instruments to request snapshot data on.

        fields: list of strings
            List of fields to request.

        convert: boolean
            If True, force numeric conversion for all values.

        Returns
        -------
            pandas.DataFrame

            pandas.DataFrame content:
                - columns : instrument and field names
                - rows : instrument name and field values

        Raises
        ------
            Exception
                If request fails or if server returns an error

            ValueError
                If a parameter type or value is wrong

        """

        if universe:
            universe = universe_arg_parser.get_list(universe)
            try:
                validate("Instrument", universe, self.universe)
            except ItemWasNotRequested as e:
                self._error(e)
                return pd.DataFrame()
        else:
            universe = self.universe

        value_by_fields_by_inst_names: dict = {}
        for name in universe:
            streaming_price: StreamingPrice = self._streaming_prices_by_name.get(name)

            values_by_fields = streaming_price.get_fields(fields)
            if values_by_fields:
                value_by_fields_by_inst_names[name] = values_by_fields

        if fields:
            try:
                self.fields and validate("Field", fields, self.fields)
            except ItemWasNotRequested as e:
                self._error(e)
                return pd.DataFrame()
        else:
            fields = get_available_fields(value_by_fields_by_inst_names)

        values_by_field = {}
        for field in fields:
            values_by_field[field] = [
                value_by_fields_by_inst_names.get(name, {}).get(field, None)
                for name in universe
            ]

        price_df = pd.DataFrame(values_by_field, columns=fields)

        if convert and not price_df.empty:
            price_df = price_df.convert_dtypes()

        universe_df = pd.DataFrame(universe, columns=["Instrument"])
        return pd.concat([universe_df, price_df], axis=1)

    def _do_pause(self) -> None:
        for streaming_price in self.values():
            streaming_price.pause()

    def _do_resume(self) -> None:
        for streaming_price in self.values():
            streaming_price.resume()

    def _do_open(self, *args, with_updates=True) -> None:
        self._debug(f"{self._classname} open streaming on {self.universe}")

        if not self.values():
            raise ValueError("No instrument to subscribe")

        self._completed.clear()

        with ThreadPoolExecutor(
            thread_name_prefix="OpenStreamingPrices-Thread"
        ) as executor:
            futures = [
                executor.submit(stream.open, with_updates=with_updates)
                for stream in self.values()
            ]
            wait(futures)
            for fut in futures:
                exception = fut.exception()
                if exception:
                    raise exception

        self._debug(f"{self._classname} streaming on {self.universe} is open")

    def _do_close(self, *args, **kwargs) -> None:
        self._debug(f"{self._classname} close streaming on {str(self.universe)}")

        with ThreadPoolExecutor(
            thread_name_prefix="CloseStreamingPrices-Thread"
        ) as executor:
            futures = [executor.submit(stream.close) for stream in self.values()]
            wait(futures)
            for fut in futures:
                exception = fut.exception()
                if exception:
                    raise exception

    def _on_stream_close(self, streaming_price: StreamingPrice) -> None:
        self._debug(f"{self._classname} streaming closed name={streaming_price.name}")
        self.close()

    def _do_on_stream_refresh(self, stream: StreamingPrice, *args) -> Tuple:
        return self._do_on_stream(stream, *args)

    def _on_stream_status(self, stream: StreamingPrice, *args) -> None:
        self._debug(f"{self._classname} on_status {args}")

        status = args[0]
        self._emitter.emit(StreamEvent.STATUS, self, stream.name, status)

        if stream.is_closed:
            self.dispatch_complete(stream)

    def _do_on_stream_update(self, stream: StreamingPrice, *args) -> Tuple:
        return self._do_on_stream(stream, *args)

    def _do_on_stream(self, stream: StreamingPrice, *args) -> Tuple:
        fields = args[0]
        return stream.name, fields

    def _on_stream_complete(self, stream: StreamingPrice, *args) -> None:
        self._debug(f"{self._classname} on_complete {args}")

        name = stream.name
        if name in self._completed:
            return

        self._completed.update([name])
        if self._completed == set(self.universe):
            # received complete event from all streams all, emit global complete
            self._emitter.emit(StreamEvent.COMPLETE, self)

    def _do_on_stream_error(self, stream: StreamingPrice, *args) -> Tuple:
        error = args[0]
        return stream.name, error


class StreamingPricesIterator:
    def __init__(self, streaming_prices: StreamingPrices):
        self._streaming_prices = streaming_prices
        self._index = 0

    def __next__(self):
        if self._index < len(self._streaming_prices.universe):
            result = self._streaming_prices[
                self._streaming_prices.universe[self._index]
            ]
            self._index += 1
            return result
        raise StopIteration()
