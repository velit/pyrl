from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, InitVar, field
from itertools import zip_longest
from random import randrange
from typing import TypeVar, Generic, Iterator

from pyrl.engine.structures.dimensions import Dimensions
from pyrl.engine.structures.helper_mixins import DimensionsMixin
from pyrl.engine.enums.directions import Coord

T = TypeVar('T')

@dataclass
class Table(Generic[T], DimensionsMixin):
    """
    Mutable non-dynamic array with two-dimensional get- and setitem methods.

    Iterating over the whole array gives all items directly by iterating the second
    dimension tighter i.e. 'line-wise' if second dimension is x.

    Underlying implementation is a one-dimensional dynamic list with dynamic methods
    disabled.
    """
    dimensions: Dimensions
    init_values: InitVar[Iterable[T]] = ()
    fillvalue: InitVar[T | None]      = None
    _impl: list[T]                    = field(init=False, repr=False)

    def __post_init__(self, init_values: Iterable[T], fillvalue: T | None) -> None:
        if fillvalue is not None:
            self._impl: list[T] = list(value for _, value in zip_longest(range(self.dimensions.area), init_values,
                                                                         fillvalue=fillvalue))
            if len(self) > self.dimensions.area:
                raise ValueError(f"Given {len(self)=} exceed {self.dimensions.area=}.")
        else:
            self._impl = list(init_values)
            if len(self) != self.dimensions.area:
                raise ValueError(f"Given {len(self)=} differs from {self.dimensions.area=} with no fillvalue")

    def __getitem__(self, coord: Coord) -> T:
        return self._impl[self.get_index(coord)]

    def __setitem__(self, coord: Coord, value: T) -> None:
        self._impl[self.get_index(coord)] = value

    def __len__(self) -> int:
        return len(self._impl)

    def __contains__(self, value: T) -> bool:
        return value in self._impl

    def __iter__(self) -> Iterator[T]:
        return iter(self._impl)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Table):
            return self.dimensions == o.dimensions and self._impl == o._impl
        return False

    def get_coord(self, index: int) -> Coord:
        return self.dimensions.get_coord(index)

    def get_index(self, coord: Coord) -> int:
        return self.dimensions.get_index(coord)

    def is_legal(self, coord: Coord) -> bool:
        y, x = coord
        return (0 <= y < self.rows) and (0 <= x < self.cols)

    def fill(self, fill_value: T) -> None:
        for i in range(self.dimensions.area):
            self[self.get_coord(i)] = fill_value

    def enumerate(self) -> Iterable[tuple[Coord, T]]:
        for i, item in enumerate(self):
            yield self.get_coord(i), item

    def coord_iter(self) -> Iterable[Coord]:
        for i, item in enumerate(self):
            yield self.get_coord(i)

    def random_coord(self) -> Coord:
        return randrange(self.rows), randrange(self.cols)
