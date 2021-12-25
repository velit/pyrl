from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True)
class Dimensions:
    rows: int
    cols: int

    @property
    def area(self) -> int:
        return self.rows * self.cols

    @property
    def min(self) -> int:
        return min(self.rows, self.cols)

    @property
    def params(self) -> tuple[int, int]:
        return self.rows, self.cols
