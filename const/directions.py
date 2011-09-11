NW = (-1, -1)
NO = (-1, 0)
NE = (-1, 1)
WE = (0, -1)
STOP = (0, 0)
EA = (0, 1)
SW = (1, -1)
SO = (1, 0)
SE = (1, 1)

ALL = (WE, SO, NO, EA, NW, NE, SW, SE, STOP)

DIAGONAL = (NW, NE, SW, SE)
ORTHOGONAL = (NO, EA, SO, WE)

rotate_clockwise = {
		NW: NO,
		NO: NE,
		NE: EA,
		EA: SE,
		SE: SO,
		SO: SW,
		SW: WE,
		WE: NW,
		}

rotate_counter_clockwise = {
		NW: WE,
		WE: SW,
		SW: SO,
		SO: SE,
		SE: EA,
		EA: NE,
		NE: NO,
		NO: NW,
		}
