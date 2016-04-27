from __future__ import absolute_import, division, print_function, unicode_literals
from bindings import Bind


class Dir(object):

    NorthWest = (-1, -1)
    North     = (-1,  0)
    NorthEast = (-1,  1)
    West      = (0,  -1)
    Stay      = (0,   0)
    East      = (0,   1)
    SouthWest = (1,  -1)
    South     = (1,   0)
    SouthEast = (1,   1)

    All = (NorthWest, North, NorthEast, West, East, SouthWest, South, SouthEast)
    AllPlusStay = (NorthWest, North, NorthEast, West, Stay, East, SouthWest, South, SouthEast)
    Diagonals = (NorthWest, NorthEast, SouthWest, SouthEast)
    Orthogonals = (North, East, South, West)

    clockwise = {
        NorthWest:  North,
        North:      NorthEast,
        NorthEast:  East,
        East:       SouthEast,
        SouthEast:  South,
        South:      SouthWest,
        SouthWest:  West,
        West:       NorthWest,
    }

    counter_clockwise = {
        NorthWest:  West,
        West:       SouthWest,
        SouthWest:  South,
        South:      SouthEast,
        SouthEast:  East,
        East:       NorthEast,
        NorthEast:  North,
        North:      NorthWest,
    }

    from_key = {}
    associate = lambda d, binds, direction: d.update((bind, direction) for bind in binds)
    associate(from_key, Bind.SouthWest + Bind.Instant_SouthWest, SouthWest)
    associate(from_key, Bind.South     + Bind.Instant_South,     South)
    associate(from_key, Bind.SouthEast + Bind.Instant_SouthEast, SouthEast)
    associate(from_key, Bind.West      + Bind.Instant_West,      West)
    associate(from_key, Bind.Stay      + Bind.Instant_Stay,      Stay)
    associate(from_key, Bind.East      + Bind.Instant_East,      East)
    associate(from_key, Bind.NorthWest + Bind.Instant_NorthWest, NorthWest)
    associate(from_key, Bind.North     + Bind.Instant_North,     North)
    associate(from_key, Bind.NorthEast + Bind.Instant_NorthEast, NorthEast)
    del associate

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
        assert False, "Invalid direction: {}".format(direction)
