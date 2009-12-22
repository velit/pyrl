import random

from square import Square
from tile import tiles

w = tiles["w"]
r = tiles["r"]
f = tiles["f"]

def init(level):
	level.map = [[Square(r,j,i) for i in range(level.cols)] for j in range(level.rows)]

def generateLevel(level):
	init(level)
	makeInitialRoom(level)
	for x in range(200):
		if random.random() < 0.50:
			attemptCorridor(level)
		else:
			attemptRoom(level)
	addUpStairCase(level)
	addDownStairCase(level)

def makeInitialRoom(level):
	while True:
		height, width = random.randrange(5,11), random.randrange(7,14)
		if height*width <= 8*8:
			break
	while True: 
		y, x = random.randrange(1,len(level.map)-height-1), \
				random.randrange(1,len(level.map[0])-width-1)
		if rectDiggable(level, y, x, height, width):
			break
	
	makeRoom(level, y, x, height, width)

def getWallSquare(level):
	while True:
		tile = level.getRandomTile()
		dir = isWall(level, tile)
		if dir[0]:
			return tile, dir[1]

def isWall(level, square):
	y,x = square.y, square.x
	if y in (0, len(level.map)-1) or x in (0, len(level.map[y])-1):
		return False, ""
	if level.getSquare(y-1,x).tile == w and level.getSquare(y+1,x).tile == w:
		if level.getSquare(y,x-1).tile == f and level.getSquare(y,x+1).tile == r:
			return True, "right"
		elif level.getSquare(y,x-1).tile == r and level.getSquare(y,x+1).tile == f:
			return True, "left"
	elif level.getSquare(y,x-1).tile == w and level.getSquare(y,x+1).tile == w:
		if level.getSquare(y-1,x).tile == f and level.getSquare(y+1,x).tile == r:
			return True, "down"
		elif level.getSquare(y-1,x).tile == r and level.getSquare(y+1,x).tile == f:
			return True, "up"
	return False, ""

def rectDiggable(level, y0, x0, height, width):
	if y0 < 0 or x0 < 0 or y0+height >= len(level.map) \
			or x0+width >= len(level.map[y0]):
		return False
	for y in range(y0, y0+height):
		for x in range(x0, x0+width):
			if level.map[y][x].tile != r and level.map[y][x].tile != w:
				return False
	return True	

def attemptRoom(level):
	square, dir = getWallSquare(level)
	y0,x0 = square.y, square.x
	height, width = random.randrange(5,11), random.randrange(7,14)
	ypos, xpos = random.choice(range(height-2)), random.choice(range(width-2))

	if dir == "left":
		y = y0 - 1 - ypos
		x = x0 - width + 1
	elif dir == "right":
		y = y0 - 1 - ypos
		x = x0
	elif dir == "up":
		y = y0 - height + 1
		x = x0 - 1 - xpos
	elif dir == "down":
		y = y0
		x = x0 - 1 - xpos

	if rectDiggable(level, y, x, height, width):
		makeRoom(level, y, x, height, width)
		level.map[y0][x0].tile = f

def makeRoom(level, y0, x0, height, width):
	for y in range(y0, y0+height):
		for x in range(x0, x0+width):
			if y in (y0, y0+height-1) or x in (x0, x0+width-1):
				level.map[y][x].tile = w
			else:
				level.map[y][x].tile = f

def digRect(level, y0, x0, tile, height=1, width=1):
	for y in range(y0, y0+height):
		for x in range(x0, x0+width):
			level.map[y][x].tile = tile

def turnRockToWall(level):
	for row in level.map:
		for col in row:
			if col.tile == r:
				col.tile = w

def attemptCorridor(level):
	square, dir = getWallSquare(level)
	y,x = square.y, square.x
	len = random.randrange(7,20)
	if dir == "up" and rectDiggable(level, y-len, x-1, len, 3) or \
			dir == "down" and rectDiggable(level, y+1, x-1, len, 3) or \
			dir == "left" and rectDiggable(level, y-1, x-len, 3, len) or \
			dir =="right" and rectDiggable(level, y-1, x+1, 3, len):
		makeCorridor(level, square, dir, len)
		return True

def makeCorridor(level, square, dir, len):
	y0,x0 = square.y, square.x

	if dir in ("up", "down"):
		fhei = whei = len
		fwid = 1
		wwid = 3
		fx = x0
		wx = x0-1
		if dir == "up":
			fy = y0-len+1
			wy = fy-1
		else:
			fy = y0
			wy = fy+1

	elif dir in ("left", "right"):
		fwid = wwid = len
		fhei = 1
		whei = 3
		fy = y0
		wy = y0-1
		if dir == "left":
			fx = x0-len+1
			wx = fx-1
		else:
			fx = x0
			wx = fx+1

	digRect(level, wy, wx, w, whei, wwid)
	digRect(level, fy, fx, f, fhei, fwid)

def addUpStairCase(level):
	while True:
		square = level.getFreeTile()
		y,x = square.y, square.x
		m = level.map
		if m[y-1][x].tile == f and m[y+1][x].tile == f and m[y][x-1].tile == f and m[y][x+1].tile == f:
			break

	square.tile = tiles["us"]
	level.squares["us"] = square

def addDownStairCase(level):
	while True:
		square = level.getFreeTile()
		y,x = square.y, square.x
		m = level.map
		if m[y-1][x].tile == f and m[y+1][x].tile == f and m[y][x-1].tile == f and m[y][x+1].tile == f:
			break

	square.tile = tiles["ds"]
	level.squares["ds"] = square
