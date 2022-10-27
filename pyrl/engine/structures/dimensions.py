from __future__ import annotations

from dataclasses import dataclass

from pyrl.engine.types.directions import Coord

@dataclass(frozen=True)
class Dimensions:
    rows: int
    cols: int

    def __post_init__(self) -> None:
        assert self.rows and self.cols, f"Zero dimensions aren't legal {self}"

    @property
    def area(self) -> int:
        return self.rows * self.cols

    @property
    def min(self) -> int:
        return min(self.rows, self.cols)

    @property
    def params(self) -> tuple[int, int]:
        return self.rows, self.cols

    def get_index(self, coord: Coord) -> int:
        row, col = coord
        if row < self.rows and col < self.cols:
            return row * self.cols + col
        raise IndexError(f"{coord=} out of range for {self=}")

    def get_coord(self, index: int) -> Coord:
        return index // self.cols, index % self.cols

