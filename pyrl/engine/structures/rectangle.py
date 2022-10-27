from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from pyrl.engine.structures.dimensions import Dimensions
from pyrl.engine.structures.helper_mixins import DimensionsMixin
from pyrl.engine.types.directions import Coord

@dataclass(init=False)
class Rectangle(DimensionsMixin):
    row_range: range
    col_range: range
    dimensions: Dimensions = field(hash=False, compare=False)

    def __init__(self, start: Coord, dimensions: Dimensions) -> None:
        """
        Accepts negative dimensions: think of them as a vector which in
        combination with start coordinate define the rectangle.

        Values stored into the Rectangle are normalized so that the upper left
        corner is always the start Coordinate and dimensions are positive
        """
        y, x = start
        rows, cols = dimensions.params
        if rows < 0:
            row_start = y + rows + 1
            row_limit = y + 1
        else:
            row_start = y
            row_limit = y + rows

        if cols < 0:
            col_start = x + cols + 1
            col_limit = x + 1
        else:
            col_start = x
            col_limit = x + cols

        self.row_range = range(row_start, row_limit)
        self.col_range = range(col_start, col_limit)
        self.dimensions = Dimensions(abs(rows), abs(cols))

    def iterate(self) -> Iterable[Coord]:
        for row in self.row_range:
            for col in self.col_range:
                yield row, col

    def enumerate_with_edge(self) -> Iterable[tuple[bool, Coord]]:
        """Return an iterable of (bool, Coord) pairs which indicate if it is an edge coordinate of the Rectangle"""
        row_edges = (self.row_range.start, self.row_range.stop - 1)
        col_edges = (self.col_range.start, self.col_range.stop - 1)
        for (row, col) in self.iterate():
            if row in row_edges or col in col_edges:
                yield True, (row, col)
            else:
                yield False, (row, col)
