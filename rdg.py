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


def generateMap(level_template):
	return MapGenerator(level_template).generate()


class MapGenerator():

	def __init__(self, level_template):
		self.rows = level_template.rows
		self.cols = level_template.cols
		self.passages = level_template.passages
		self.canvas = Map(TileMap(self.rows, self.cols, ROCK))

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

	def add_staircase_up(self):
		while True:
			square = self.canvas.get_free_square()
			y, x = square.y, square.x
			g = self.canvas.getsquare
			if g(y - 1, x).tile == f and g(y + 1, x).tile == f \
					and g(y, x - 1).tile == f and g(y, x + 1).tile == f:
				break

		square.tile = us
		self.canvas.entrance_squares[PASSAGE_UP] = square


	def add_staircase_down(self):
		while True:
			square = self.canvas.get_free_square()
			y, x = square.y, square.x
			g = self.canvas.getsquare
			if g(y - 1, x).tile == f and g(y + 1, x).tile == f and \
					g(y, x - 1).tile == f and g(y, x + 1).tile == f:
				break

		square.tile = ds
		self.canvas.entrance_squares[PASSAGE_DOWN] = square


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


	def _get_wall_square(self):
		while True:
			square = self.canvas.get_random_square()
			dir = self._is_wall(square)
			if dir[0]:
				return square, dir[1]


	def _is_wall(self, square):
		y, x = square.y, square.x
		g = self.canvas.getsquare
		if y in (0, self.rows - 1) or x in (0, self.cols - 1):
			return False, ""
		if g(y - 1, x).tile == w and g(y + 1, x).tile == w:
			if g(y, x - 1).tile == f and g(y, x + 1).tile == r:
				return True, "right"
			elif g(y, x - 1).tile == r and g(y, x + 1).tile == f:
				return True, "left"
		elif g(y, x - 1).tile == w and g(y, x + 1).tile == w:
			if g(y - 1, x).tile == f and g(y + 1, x).tile == r:
				return True, "down"
			elif g(y - 1, x).tile == r and g(y + 1, x).tile == f:
				return True, "up"
		return False, ""


	def _rect_diggable(self, y0, x0, height, width):
		if y0 < 0 or x0 < 0 or y0 + height >= self.rows \
				or x0 + width >= self.cols:
			return False
		for y in range(y0, y0 + height):
			for x in range(x0, x0 + width):
				if self.canvas.getsquare(y, x).tile != r and \
						self.canvas.getsquare(y, x).tile != w:
					return False
		return True


	def _attempt_room(self):
		square, dir = self._get_wall_square()
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

		if self._rect_diggable(y, x, height, width):
			self._make_room(y, x, height, width)
			self.canvas.getsquare(y0, x0).tile = f


	def _make_room(self, y0, x0, height, width):
		for y in range(y0, y0 + height):
			for x in range(x0, x0 + width):
				if y in (y0, y0 + height - 1) or x in (x0, x0 + width - 1):
					self.canvas.getsquare(y, x).tile = w
				else:
					self.canvas.getsquare(y, x).tile = f


	def _dig_rect(self, y0, x0, tile, height=1, width=1):
		for y in range(y0, y0 + height):
			for x in range(x0, x0 + width):
				self.canvas.getsquare(y, x).tile = tile


	def _turn_rock_to_wall(self):
		for square in self.canvas:
				if square.tile == r:
					square.tile = w


	def _attempt_corridor(self):
		square, dir = self._get_wall_square()
		y, x = square.y, square.x
		len = rr(7, 20)
		if dir == "up" and self._rect_diggable(y - len, x - 1, len, 3) or \
				dir == "down" and self._rect_diggable(y + 1, x - 1, len, 3) or \
				dir == "left" and self._rect_diggable(y - 1, x - len, 3, len) or \
				dir == "right" and self._rect_diggable(y - 1, x + 1, 3, len):
			self._make_corridor(square, dir, len)
			return True


	def _make_corridor(self, square, dir, len):
		y0, x0 = square.y, square.x

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
