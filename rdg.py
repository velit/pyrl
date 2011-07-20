from random import randrange as rr, random as rand, choice

from map_file import MapFile
from tiles import WALL, ROCK, FLOOR, STAIRS_UP, STAIRS_DOWN, gettile
from const.game import PASSAGE_DOWN, PASSAGE_UP

w = WALL
r = ROCK
f = FLOOR
us = STAIRS_UP
ds = STAIRS_DOWN


def generateMap(rows, cols, passages):
	return MapGenerator(rows, cols, passages).generate()


class MapGenerator:

	def __init__(self, rows, cols, passages):
		self.rows = rows
		self.cols = cols
		self.passages = passages
		self.canvas = MapFile(rows, cols, ROCK)

	def generate(self):
		self._make_initial_room()
		for x in range(2000):
			if rand() < 0.50:
				self._attempt_corridor()
			else:
				self._attempt_room()
		if PASSAGE_UP in self.passages:
			self.add_staircase_up()
		if PASSAGE_DOWN in self.passages:
			self.add_staircase_down()
		return self.canvas

	def get_free_loc(self):
		while True:
			y, x = self.get_random_loc()
			if self.canvas.gettile(y, x).passable:
				return y, x

	def get_random_loc(self):
		return rr(self.canvas.rows), rr(self.canvas.cols)

	def add_staircase_up(self):
		while True:
			y, x = self.get_free_loc()
			g = self.canvas.get_tile_id
			if g(y - 1, x) == f and g(y + 1, x) == f \
					and g(y, x - 1) == f and g(y, x + 1) == f:
				break

		self.canvas.set_tile_id(y, x, us)
		self.canvas.entrance_coords[PASSAGE_UP] = (y, x)

	def add_staircase_down(self):
		while True:
			y, x = self.get_free_loc()
			g = self.canvas.get_tile_id
			if g(y - 1, x) == f and g(y + 1, x) == f and \
					g(y, x - 1) == f and g(y, x + 1) == f:
				break

		self.canvas.set_tile_id(y, x, ds)
		self.canvas.entrance_coords[PASSAGE_DOWN] = (y, x)

	def _make_initial_room(self):
		while True:
			height, width = rr(5, 11), rr(7, 14)
			if height * width <= 8 * 8:
				break
		while True:
			y, x = rr(1, self.rows - height - 1), rr(1, self.cols - width - 1)
			if self._rect_diggable(y, x, height, width):
				break

		self._make_room(y, x, height, width)

	def _get_wall_loc(self):
		while True:
			y, x = self.get_random_loc()
			dir = self._is_wall(y, x)
			if dir[0]:
				return y, x, dir[1]

	def _is_wall(self, y, x):
		g = self.canvas.get_tile_id
		if y in (0, self.rows - 1) or x in (0, self.cols - 1):
			return False, ""
		if g(y - 1, x) == w and g(y + 1, x) == w:
			if g(y, x - 1) == f and g(y, x + 1) == r:
				return True, "right"
			elif g(y, x - 1) == r and g(y, x + 1) == f:
				return True, "left"
		elif g(y, x - 1) == w and g(y, x + 1) == w:
			if g(y - 1, x) == f and g(y + 1, x) == r:
				return True, "down"
			elif g(y - 1, x) == r and g(y + 1, x) == f:
				return True, "up"
		return False, ""

	def _rect_diggable(self, y0, x0, height, width):
		if y0 < 0 or x0 < 0 or y0 + height >= self.rows \
				or x0 + width >= self.cols:
			return False
		for y in range(y0, y0 + height):
			for x in range(x0, x0 + width):
				if self.canvas.get_tile_id(y, x) != r and \
						self.canvas.get_tile_id(y, x) != w:
					return False
		return True

	def _attempt_room(self):
		y0, x0, dir = self._get_wall_loc()
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

		if self._rect_diggable(y, x, height, width):
			self._make_room(y, x, height, width)
			self.canvas.set_tile_id(y0, x0, f)

	def _make_room(self, y0, x0, height, width):
		for y in range(y0, y0 + height):
			for x in range(x0, x0 + width):
				if y in (y0, y0 + height - 1) or x in (x0, x0 + width - 1):
					self.canvas.set_tile_id(y, x, w)
				else:
					self.canvas.set_tile_id(y, x, f)

	def _dig_rect(self, y0, x0, tile, height=1, width=1):
		for y in range(y0, y0 + height):
			for x in range(x0, x0 + width):
				self.canvas.set_tile_id(y, x, tile)

	def _turn_rock_to_wall(self):
		self.canvas.tilemap = [w if x == r else x for x in self.canvas.tilemap]

	def _attempt_corridor(self):
		y, x, dir = self._get_wall_loc()
		len = rr(7, 20)
		if dir == "up" and self._rect_diggable(y - len, x - 1, len, 3) or \
				dir == "down" and self._rect_diggable(y + 1, x - 1, len, 3) or \
				dir == "left" and self._rect_diggable(y - 1, x - len, 3, len) or \
				dir == "right" and self._rect_diggable(y - 1, x + 1, 3, len):
			self._make_corridor(y, x, dir, len)
			return True

	def _make_corridor(self, y0, x0, dir, len):
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

		self._dig_rect(wy, wx, w, whei, wwid)
		self._dig_rect(fy, fx, f, fhei, fwid)
