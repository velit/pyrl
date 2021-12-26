from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True)
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

