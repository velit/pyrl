import string

OPTIMIZATION = False
DEBUG = False

YES = set((ord('y'), ord('Y')))
NO = set((ord('n'), ord('N')))
DEFAULT = set((ord('\n'), ord(' ')))
MOVES = set(map(ord, tuple(string.digits))); MOVES.add(ord('.'))

SW = 1; S = 2; SE = 3; W = 4; STOP = 5; E = 6; NW = 7; N = 8; NE = 9
UP = (NW, N, NE)
DOWN = (SW, S, SE)
LEFT = (SW, W, NW)
RIGHT = (SE, E, NE)

DY = {}
DX = {}
DY[STOP] = 0
DX[STOP] = 0
for dir in range(1, 1+9):
	DY[dir] = 0
	DX[dir] = 0
	if dir in UP:
		DY[dir] -= 1
	elif dir in DOWN:
		DY[dir] += 1
	if dir in LEFT:
		DX[dir] -= 1
	elif dir in RIGHT:
		DX[dir] += 1
