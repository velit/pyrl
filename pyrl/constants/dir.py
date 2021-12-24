from __future__ import annotations

from collections.abc import Iterable, MutableMapping
from typing import Any, Literal

from pyrl.binds import Binds, Bind

DirectionUnit = Literal[-1, 0, 1]
Direction = tuple[DirectionUnit, DirectionUnit]
Directions = tuple[Direction, ...]

All: Directions = (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)
(                NorthWest, North,    NorthEast, East,     SouthEast, South,    SouthWest, West) = All
Stay: Direction = (0, 0)
AllPlusStay: Directions = All + (Stay,)
Diagonals:   Directions = NorthWest, NorthEast, SouthEast, SouthWest
Orthogonals: Directions = North, East, South, West

OrthogonalMoveMult = 1.0
DiagonalMoveMult = 2 ** 0.5
StayMoveMult = 1.0

def move_mult(direction: Direction) -> float:
    if direction in Orthogonals:
        return OrthogonalMoveMult
    elif direction in Diagonals:
        return DiagonalMoveMult
    elif direction == Stay:
        return StayMoveMult
    assert False, f"Invalid {direction=}"

def clockwise(direction: Direction) -> Direction:
    return All[(All.index(direction) + 1) % len(All)]

def counter_clockwise(direction: Direction) -> Direction:
    return All[(All.index(direction) - 1) % len(All)]

from_key: dict[Bind, Direction] = {}

def init_from_key() -> None:
    def set_every_to(every: Iterable, to: Any, at: MutableMapping) -> None:
        for item in every:
            at[item] = to

    set_every_to(Binds.SouthWest + Binds.Instant_SouthWest, to=SouthWest, at=from_key)
    set_every_to(Binds.South + Binds.Instant_South,         to=South,     at=from_key)
    set_every_to(Binds.SouthEast + Binds.Instant_SouthEast, to=SouthEast, at=from_key)
    set_every_to(Binds.West + Binds.Instant_West,           to=West,      at=from_key)
    set_every_to(Binds.Stay + Binds.Instant_Stay,           to=Stay,      at=from_key)
    set_every_to(Binds.East + Binds.Instant_East,           to=East,      at=from_key)
    set_every_to(Binds.NorthWest + Binds.Instant_NorthWest, to=NorthWest, at=from_key)
    set_every_to(Binds.North + Binds.Instant_North,         to=North,     at=from_key)
    set_every_to(Binds.NorthEast + Binds.Instant_NorthEast, to=NorthEast, at=from_key)
    global init_from_key
    del init_from_key
init_from_key()
