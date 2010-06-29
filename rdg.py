from random import randrange as rr, random as rand, choice

from square import Square as S
from tile import tiles

w = tiles["w"]
r = tiles["r"]
f = tiles["f"]

def init(level):
	y, x = level.rows, level.cols
	level.map = [S(r, i / x, i % x) for i in range(y * x)]

def generateLevel(level):
	init(level)
	makeInitialRoom(level)
	for x in range(2000):
		if rand() < 0.50:
			attemptCorridor(level)
		else:
			attemptRoom(level)
	addUpStairCase(level)
	addDownStairCase(level)

def makeInitialRoom(level):
	while True:
		height, width = rr(5, 11), rr(7, 14)
		if height*width <= 8*8:
			break
	while True: 
		y, x = rr(1, level.rows-height-1), rr(1, level.cols-width-1)
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
	y, x = square.y, square.x
	g = level.getSquare
	if y in (0, level.rows-1) or x in (0, level.cols-1):
		return False, ""
	if g(y-1, x).tile == w and g(y+1, x).tile == w:
		if g(y, x-1).tile == f and g(y, x+1).tile == r:
			return True, "right"
		elif g(y, x-1).tile == r and g(y, x+1).tile == f:
			return True, "left"
	elif g(y, x-1).tile == w and g(y, x+1).tile == w:
		if g(y-1, x).tile == f and g(y+1, x).tile == r:
			return True, "down"
		elif g(y-1, x).tile == r and g(y+1, x).tile == f:
			return True, "up"
	return False, ""

def rectDiggable(level, y0, x0, height, width):
	if y0 < 0 or x0 < 0 or y0+height >= level.rows \
			or x0+width >= level.cols:
		return False
	for y in range(y0, y0+height):
		for x in range(x0, x0+width):
			if level.getSquare(y, x).tile != r and \
					level.getSquare(y, x).tile != w:
				return False
	return True	

def attemptRoom(level):
	square, dir = getWallSquare(level)
	y0, x0 = square.y, square.x
	height, width = rr(5, 11), rr(7, 14)
	ypos, xpos = choice(range(height-2)), choice(range(width-2))

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
		level.getSquare(y0, x0).tile = f

def makeRoom(level, y0, x0, height, width):
	for y in range(y0, y0+height):
		for x in range(x0, x0+width):
			if y in (y0, y0+height-1) or x in (x0, x0+width-1):
				level.getSquare(y, x).tile = w
			else:
				level.getSquare(y, x).tile = f

def digRect(level, y0, x0, tile, height=1, width=1):
	for y in range(y0, y0+height):
		for x in range(x0, x0+width):
			level.getSquare(y, x).tile = tile

def turnRockToWall(level):
	for square in level.map:
			if square.tile == r:
				square.tile = w

def attemptCorridor(level):
	square, dir = getWallSquare(level)
	y, x = square.y, square.x
	len = rr(7, 20)
	if dir == "up" and rectDiggable(level, y-len, x-1, len, 3) or \
			dir == "down" and rectDiggable(level, y+1, x-1, len, 3) or \
			dir == "left" and rectDiggable(level, y-1, x-len, 3, len) or \
			dir =="right" and rectDiggable(level, y-1, x+1, 3, len):
		makeCorridor(level, square, dir, len)
		return True

def makeCorridor(level, square, dir, len):
	y0, x0 = square.y, square.x

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
		y, x = square.y, square.x
		g = level.getSquare
		if g(y-1, x).tile == f and g(y+1, x).tile == f \
				and g(y, x-1).tile == f and g(y, x+1).tile == f:
			break

	square.tile = tiles["us"]
	level.squares["us"] = square

def addDownStairCase(level):
	while True:
		square = level.getFreeTile()
		y, x = square.y, square.x
		g = level.getSquare
		if g(y-1, x).tile == f and g(y+1, x).tile == f and \
				g(y, x-1).tile == f and g(y, x+1).tile == f:
			break

	square.tile = tiles["ds"]
	level.squares["ds"] = square
