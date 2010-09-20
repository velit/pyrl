from random import randrange as rr, random as rand, choice

from map import Map
from dummy_map import DummyMap
from square import Square as S
from tile import tiles

w = tiles["w"]
r = tiles["r"]
f = tiles["f"]

def generateLevel(level):
	level.map = Map(DummyMap(level.rows, level.cols, "r"))
	_make_initial_room(level)
	for x in range(2000):
		if rand() < 0.50:
			_attempt_corridor(level)
		else:
			_attempt_room(level)
	add_staircase_up(level)
	add_staircase_down(level)

def add_staircase_up(level):
	while True:
		square = level.get_free_tile()
		y, x = square.y, square.x
		g = level.getsquare
		if g(y-1, x).tile == f and g(y+1, x).tile == f \
				and g(y, x-1).tile == f and g(y, x+1).tile == f:
			break

	square.tile = tiles["us"]
	level.map.squares["us"] = square

def add_staircase_down(level):
	while True:
		square = level.get_free_tile()
		y, x = square.y, square.x
		g = level.getsquare
		if g(y-1, x).tile == f and g(y+1, x).tile == f and \
				g(y, x-1).tile == f and g(y, x+1).tile == f:
			break

	square.tile = tiles["ds"]
	level.map.squares["ds"] = square

def _make_initial_room(level):
	while True:
		height, width = rr(5, 11), rr(7, 14)
		if height*width <= 8*8:
			break
	while True: 
		y, x = rr(1, level.rows-height-1), rr(1, level.cols-width-1)
		if _rect_diggable(level, y, x, height, width):
			break
	
	_make_room(level, y, x, height, width)

def _get_wall_square(level):
	while True:
		tile = level.get_random_tile()
		dir = _is_wall(level, tile)
		if dir[0]:
			return tile, dir[1]

def _is_wall(level, square):
	y, x = square.y, square.x
	g = level.getsquare
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

def _rect_diggable(level, y0, x0, height, width):
	if y0 < 0 or x0 < 0 or y0+height >= level.rows \
			or x0+width >= level.cols:
		return False
	for y in range(y0, y0+height):
		for x in range(x0, x0+width):
			if level.getsquare(y, x).tile != r and \
					level.getsquare(y, x).tile != w:
				return False
	return True	

def _attempt_room(level):
	square, dir = _get_wall_square(level)
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

	if _rect_diggable(level, y, x, height, width):
		_make_room(level, y, x, height, width)
		level.getsquare(y0, x0).tile = f

def _make_room(level, y0, x0, height, width):
	for y in range(y0, y0+height):
		for x in range(x0, x0+width):
			if y in (y0, y0+height-1) or x in (x0, x0+width-1):
				level.getsquare(y, x).tile = w
			else:
				level.getsquare(y, x).tile = f

def _dig_rect(level, y0, x0, tile, height=1, width=1):
	for y in range(y0, y0+height):
		for x in range(x0, x0+width):
			level.getsquare(y, x).tile = tile

def _turn_rock_to_wall(level):
	for square in level.map:
			if square.tile == r:
				square.tile = w

def _attempt_corridor(level):
	square, dir = _get_wall_square(level)
	y, x = square.y, square.x
	len = rr(7, 20)
	if dir == "up" and _rect_diggable(level, y-len, x-1, len, 3) or \
			dir == "down" and _rect_diggable(level, y+1, x-1, len, 3) or \
			dir == "left" and _rect_diggable(level, y-1, x-len, 3, len) or \
			dir =="right" and _rect_diggable(level, y-1, x+1, 3, len):
		_make_corridor(level, square, dir, len)
		return True

def _make_corridor(level, square, dir, len):
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

	_dig_rect(level, wy, wx, w, whei, wwid)
	_dig_rect(level, fy, fx, f, fhei, fwid)
