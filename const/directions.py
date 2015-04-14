from __future__ import absolute_import, division, print_function, unicode_literals


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
