import const.game as GAME
import const.generated_level_types as LEVEL_TYPE
import const.tiles as TILE

from random import randrange as rr, random as rand
from const.tiles import WALL as W
from const.tiles import ROCK as R
from const.tiles import FLOOR as F


def add_generated_tilefile(level_file, level_type=LEVEL_TYPE.ARENA):
	if level_type == LEVEL_TYPE.DUNGEON:
		if level_file.tilefile is None:
			_init_tilemap(level_file)
			_make_initial_room(level_file)
		else:
			level_file.add_walls()

		for x in xrange(GAME.RDG_LEVEL_PASSES):
			if rand() < 0.50:
				_attempt_corridor(level_file)
			else:
				_attempt_room(level_file)
	elif level_type == LEVEL_TYPE.ARENA:
		_init_tilemap(level_file)
		_make_room(level_file, 0, 0, level_file.rows, level_file.cols)

	if GAME.PASSAGE_UP not in level_file.passage_locations:
		add_passageway(level_file, GAME.PASSAGE_UP, TILE.STAIRS_UP)
	if GAME.PASSAGE_DOWN not in level_file.passage_locations:
		add_passageway(level_file, GAME.PASSAGE_DOWN, TILE.STAIRS_DOWN)

def get_free_coord(level_file):
	while True:
		y, x = get_random_coord(level_file)
		if level_file.get_tile_from_coord(y, x).is_passable:
			return y, x

def get_random_coord(level_file):
	return rr(level_file.rows), rr(level_file.cols)

def add_passageway(level_file, passage, passage_tile_id):
	while True:
		y, x = get_free_coord(level_file)
		g = level_file.get_tile_id
		if g(y - 1, x) == F and g(y + 1, x) == F \
				and g(y, x - 1) == F and g(y, x + 1) == F and g(y, x) == F:
			break

	level_file.set_tile_id(y, x, passage_tile_id)
	level_file.passage_locations[passage] = y, x

def _init_tilemap(level_file):
	level_file.tilefile = [R for x in xrange(level_file.rows * level_file.cols)]

def _make_initial_room(level_file):
	while True:
		height, width = rr(5, 11), rr(7, 14)
		if height * width <= 8 * 8:
			break
	while True:
		y, x = rr(1, level_file.rows - height - 1), rr(1, level_file.cols - width - 1)
		if _rect_diggable(level_file, y, x, height, width):
			break

	_make_room(level_file, y, x, height, width)

def _get_wall_coord(level_file):
	while True:
		y, x = get_random_coord(level_file)
		dir = _is_wall(level_file, y, x)
		if dir[0]:
			return y, x, dir[1]

def _is_wall(level_file, y, x):
	g = level_file.get_tile_id
	if y in (0, level_file.rows - 1) or x in (0, level_file.cols - 1):
		return False, ""
	if g(y - 1, x) == W and g(y + 1, x) == W:
		if g(y, x - 1) == F and g(y, x + 1) == R:
			return True, "right"
		elif g(y, x - 1) == R and g(y, x + 1) == F:
			return True, "left"
	elif g(y, x - 1) == W and g(y, x + 1) == W:
		if g(y - 1, x) == F and g(y + 1, x) == R:
			return True, "down"
		elif g(y - 1, x) == R and g(y + 1, x) == F:
			return True, "up"
	return False, ""

def _rect_diggable(level_file, y0, x0, height, width):
	if y0 < 0 or x0 < 0 or y0 + height >= level_file.rows \
			or x0 + width >= level_file.cols:
		return False
	for y in xrange(y0, y0 + height):
		for x in xrange(x0, x0 + width):
			if level_file.get_tile_id(y, x) != R and \
					level_file.get_tile_id(y, x) != W:
				return False
	return True

def _attempt_room(level_file):
	y0, x0, dir = _get_wall_coord(level_file)
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

	if _rect_diggable(level_file, y, x, height, width):
		_make_room(level_file, y, x, height, width)
		level_file.set_tile_id(y0, x0, F)

def _make_room(level_file, y0, x0, height, width):
	for y in xrange(y0, y0 + height):
		for x in xrange(x0, x0 + width):
			if y in (y0, y0 + height - 1) or x in (x0, x0 + width - 1):
				level_file.set_tile_id(y, x, W)
			else:
				level_file.set_tile_id(y, x, F)

def _dig_rect(level_file, y0, x0, tile, height=1, width=1):
	for y in xrange(y0, y0 + height):
		for x in xrange(x0, x0 + width):
			level_file.set_tile_id(y, x, tile)

def _turn_rock_to_wall(level_file):
	level_file.tilefile = [W if x == R else x for x in level_file.tilefile]

def _attempt_corridor(level_file):
	y, x, dir = _get_wall_coord(level_file)
	len = rr(7, 20)
	if dir == "up" and _rect_diggable(level_file, y - len, x - 1, len, 3) or \
			dir == "down" and _rect_diggable(level_file, y + 1, x - 1, len, 3) or \
			dir == "left" and _rect_diggable(level_file, y - 1, x - len, 3, len) or \
			dir == "right" and _rect_diggable(level_file, y - 1, x + 1, 3, len):
		_make_corridor(level_file, y, x, dir, len)
		return True

def _make_corridor(level_file, y0, x0, dir, len):
	if dir in ("up", "down"):
		fhei = whei = len
		fwid = 1
		wwid = 3
		fx = x0
		wx = x0-1
		if dir == "up":
			fy = y0 - len + 1
			wy = fy - 1
		else:
			fy = y0
			wy = fy + 1

	elif dir in ("left", "right"):
		fwid = wwid = len
		fhei = 1
		whei = 3
		fy = y0
		wy = y0-1
		if dir == "left":
			fx = x0 - len + 1
			wx = fx - 1
		else:
			fx = x0
			wx = fx + 1

	_dig_rect(level_file, wy, wx, W, whei, wwid)
	_dig_rect(level_file, fy, fx, F, fhei, fwid)
