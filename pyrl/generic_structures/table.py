from __future__ import annotations

from collections.abc import Iterable
from itertools import zip_longest
from random import randrange
from typing import TypeVar, Generic, Iterator, Generator

from pyrl.constants.coord import Coord
from pyrl.generic_structures.dimensions import Dimensions

T = TypeVar('T')
class Table(Generic[T]):
    """
    Mutable non-dynamic array with two-dimensional get- and setitem methods.

    Iterating over the whole array gives all items directly by iterating the second
    dimension tighter i.e. 'line-wise' if second dimension is x.

    Underlying implementation is a one-dimensional dynamic list with dynamic methods
    disabled.
    """
    def __init__(self, dimensions: Dimensions, init_values: Iterable[T] = (), fillvalue: T | None = None):
        self.dimensions: Dimensions = dimensions
        self._impl: list[T] = list(value for _, value in zip_longest(range(self.dimensions.area), init_values,
                                                                     fillvalue=fillvalue))
        assert len(self) <= dimensions.area, f"Given {len(self)=} exceed {self.dimensions.area=}."

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
        return self.get_coord_from_index(index, self.dimensions.cols)

    def get_index(self, coord: Coord) -> int:
        return self.get_index_from_coord(coord, self.dimensions.cols)

    def is_legal(self, coord: Coord) -> bool:
        y, x = coord
        return (0 <= y < self.rows) and (0 <= x < self.cols)

    def clear(self) -> None:
        for i in range(self.dimensions.area):
            self[self.get_coord(i)] = None

    def enumerate(self) -> Generator[tuple[Coord, T], None, None]:
        for i, item in enumerate(self):
            yield self.get_coord(i), item

    def coord_iter(self) -> Generator[Coord, None, None]:
        for i, item in enumerate(self):
            yield self.get_coord(i)

    def random_coord(self) -> Coord:
        return randrange(self.rows), randrange(self.cols)

    @property
    def rows(self) -> int:
        return self.dimensions.rows

    @property
    def cols(self) -> int:
        return self.dimensions.cols

    @staticmethod
    def get_index_from_coord(coord: Coord, second_dim_bound: int) -> int:
        first_dim, second_dim = coord
        if second_dim < second_dim_bound:
            return first_dim * second_dim_bound + second_dim
        else:
            raise IndexError(f"Second dimension index out of range: {second_dim=} < {second_dim_bound=}")

    @staticmethod
    def get_coord_from_index(index: int, second_dim_bound: int) -> Coord:
        return index // second_dim_bound, index % second_dim_bound
