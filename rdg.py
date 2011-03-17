from random import randrange as rr, random as rand, choice

from map import Map, TileMap
from square import Square as S
from tiles import gettile, WALL, ROCK, FLOOR, STAIRS_UP, STAIRS_DOWN
from const.game import PASSAGE_DOWN, PASSAGE_UP

w = gettile(WALL)
r = gettile(ROCK)
f = gettile(FLOOR)
us = gettile(STAIRS_UP)
ds = gettile(STAIRS_DOWN)

def generateLevel(level, passages):
	level.map = Map(TileMap(level.rows, level.cols, "r"))
	_make_initial_room(level)
	for x in range(2000):
		if rand() < 0.50:
			_attempt_corridor(level)
		else:
			_attempt_room(level)
	if PASSAGE_UP in passages:
		add_staircase_up(level)
	if PASSAGE_DOWN in passages:
		add_staircase_down(level)

def add_staircase_up(level):
	while True:
		square = level.get_free_square()
		y, x = square.y, square.x
		g = level.getsquare
		if g(y-1, x).tile == f and g(y+1, x).tile == f \
				and g(y, x-1).tile == f and g(y, x+1).tile == f:
			break

	square.tile = us
	level.map.entrance_squares[PASSAGE_UP] = square

def add_staircase_down(level):
	while True:
		square = level.get_free_square()
		y, x = square.y, square.x
		g = level.getsquare
		if g(y-1, x).tile == f and g(y+1, x).tile == f and \
				g(y, x-1).tile == f and g(y, x+1).tile == f:
			break

	square.tile = ds
	level.map.entrance_squares[PASSAGE_DOWN] = square

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
		square = level.get_random_square()
		dir = _is_wall(level, square)
		if dir[0]:
			return square, dir[1]

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
	ypos, xpos = rr(height-2), rr(width-2)

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
