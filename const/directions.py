SW = "southwest"
SO = "south"
SE = "southeast"
WE = "west"
EA = "east"
NW = "northwest"
NO = "north"
NE = "northeast"
STOP = "current position"

ALL_DIRECTIONS = (SW, SO, SE, WE, EA, NW, NO, NE)

UP = (NW, NO, NE)
DOWN = (SW, SO, SE)
LEFT = (SW, WE, NW)
RIGHT = (SE, EA, NE)

DIAGONAL = (NW, NE, SW, SE)
ORTHOGONAL = (NO, EA, SO, WE)

DELTA = {
		SW: (1, -1),
		SO: (1, 0),
		SE: (1, 1),
		WE: (0, -1),
		EA: (0, 1),
		NW: (-1, -1),
		NO: (-1, 0),
		NE: (-1, 1),
		STOP: (0, 0),
}
