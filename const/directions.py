SW = 1
SO = 2
SE = 3
WE = 4
STOP = 5
EA = 6
NW = 7
NO = 8
NE = 9

UP = (NW, NO, NE)
DOWN = (SW, SO, SE)
LEFT = (SW, WE, NW)
RIGHT = (SE, EA, NE)

DELTA = {
	SW: (1, -1),
	SO: (1, 0),
	SE: (1, 1),
	WE: (0, -1),
	STOP: (0, 0),
	EA: (0, 1),
	NW: (-1, -1),
	NO: (-1, 0),
	NE: (-1, 1),
}
