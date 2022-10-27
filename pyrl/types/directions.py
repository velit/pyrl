from __future__ import annotations

from typing import Literal, Final

Coord = tuple[int, int]
DirectionUnit = Literal[-1, 0, 1]
Direction     = tuple[DirectionUnit, DirectionUnit]
Directions    = tuple[Direction, ...]

class Dir:
    OrthogonalMoveMult: Final[float] = 1.0
    DiagonalMoveMult:   Final[float] = 2 ** 0.5
    StayMoveMult:       Final[float] = 1.0
    Stay:           Final[Direction] = ( 0,  0)
    North:          Final[Direction] = (-1,  0)
    NorthEast:      Final[Direction] = (-1,  1)
    East:           Final[Direction] = ( 0,  1)
    SouthEast:      Final[Direction] = ( 1,  1)
    South:          Final[Direction] = ( 1,  0)
    SouthWest:      Final[Direction] = ( 1, -1)
    West:           Final[Direction] = ( 0, -1)
    NorthWest:      Final[Direction] = (-1, -1)
    Diagonals:     Final[Directions] = NorthEast, SouthEast, SouthWest, NorthWest
    Orthogonals:   Final[Directions] = North, East, South, West
    All:           Final[Directions] = North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
    AllPlusStay:   Final[Directions] = All + (Stay,)

    @classmethod
    def clockwise(cls, direction: Direction, turns: int = 1) -> Direction:
        return cls.All[(cls.All.index(direction) + turns) % len(cls.All)]

    @classmethod
    def counter_clockwise(cls, direction: Direction, turns: int = 1) -> Direction:
        return cls.All[(cls.All.index(direction) - turns) % len(cls.All)]
