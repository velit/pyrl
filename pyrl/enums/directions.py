from typing import Tuple, Dict, Iterable, Any, MutableMapping

from pyrl.binds import Binds, Bind

Direction = Tuple[int, int]

def set_every_to(every: Iterable, to: Any, at: MutableMapping):
    for item in every:
        at[item] = to

class Dir:

    All = (-1, -1),  (-1,  0), (-1,  1),  (0,   1), (1,   1),  (1,   0), (1,  -1),  (0,  -1)
    (     NorthWest, North,    NorthEast, East,     SouthEast, South,    SouthWest, West) = All
    Stay = (0, 0)
    AllPlusStay = All + (Stay, )
    Diagonals = NorthWest, NorthEast, SouthEast, SouthWest
    Orthogonals = North, East, South, West

    @classmethod
    def clockwise(cls, direction: Tuple[int, int]):
        return cls.All[(cls.All.index(direction) + 1) % len(cls.All)]

    @classmethod
    def counter_clockwise(cls, direction: Tuple[int, int]):
        return cls.All[(cls.All.index(direction) - 1) % len(cls.All)]

    from_key: Dict[Bind, Direction] = {}
    set_every_to(Binds.SouthWest + Binds.Instant_SouthWest, to=SouthWest, at=from_key)
    set_every_to(Binds.South     + Binds.Instant_South,     to=South,     at=from_key)
    set_every_to(Binds.SouthEast + Binds.Instant_SouthEast, to=SouthEast, at=from_key)
    set_every_to(Binds.West      + Binds.Instant_West,      to=West,      at=from_key)
    set_every_to(Binds.Stay      + Binds.Instant_Stay,      to=Stay,      at=from_key)
    set_every_to(Binds.East      + Binds.Instant_East,      to=East,      at=from_key)
    set_every_to(Binds.NorthWest + Binds.Instant_NorthWest, to=NorthWest, at=from_key)
    set_every_to(Binds.North     + Binds.Instant_North,     to=North,     at=from_key)
    set_every_to(Binds.NorthEast + Binds.Instant_NorthEast, to=NorthEast, at=from_key)

    OrthogonalMoveMult = 1
    DiagonalMoveMult = 2 ** 0.5
    StayMoveMult = 1

    @classmethod
    def move_mult(cls, direction):
        if direction in cls.Orthogonals:
            return cls.OrthogonalMoveMult
        elif direction in cls.Diagonals:
            return cls.DiagonalMoveMult
        elif direction == cls.Stay:
            return cls.StayMoveMult
        assert False, f"Invalid {direction=}"
