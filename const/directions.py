SW = 1
S = 2
SE = 3
W = 4
STOP = 5
E = 6
NW = 7
N = 8
NE = 9

UP = (NW, N, NE)
DOWN = (SW, S, SE)
LEFT = (SW, W, NW)
RIGHT = (SE, E, NE)

DY = {}
DX = {}
DX[STOP] = 0
for dir in range(1, 9 + 1):
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
