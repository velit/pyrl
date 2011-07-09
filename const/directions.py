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
