import random

from tiles import gettile, FLOOR
from const.game import PASSAGE_RANDOM


class Map:
	"""Actual map data structure used in-game containing Squares."""

	def __init__(self, map_file):
		self.rows = map_file.rows
		self.cols = map_file.cols
		self.tiles = [gettile(k, map_file.tile_dict) for k in map_file.tilemap]
		self.creatures = {}
		self.entrance_locations = {}

		for key, y, x in map_file.entrance_coords.items():
			self.entrance_locations[key] = y, x

	def get_entrance_loc(self, entrance):
		if entrance == PASSAGE_RANDOM:
			return self.get_free_square()
		else:
			return self.entrance_locations[entrance]

	def get_free_loc(self):
		while True:
			loc = self.get_random_loc()
			if self.passable(loc):
				return loc

	def get_random_loc(self):
		return random.randrange(len(self.tiles))

	def passable(self, loc):
		if loc in self.creatures:
			return False
		else:
			return self.tiles[loc].passable

	def see_through(self, loc):
		return self.tiles[loc].see_through

	def get_visible_char_data(self, loc, shift=""):
		if loc in self.creatures:
			symbol, color = self.creatures[loc].char
		else:
			symbol, color = self.tiles[loc].visible_char
		return symbol, color + color_shift

	def get_memory_char_data(self, loc, shift=""):
		symbol, color = self.tiles[loc].memory_char
		return symbol, color + shift

	def isexit(self, loc):
		return self.tiles[loc].exit_point is not None

	def getexit(self):
		return self.tiles[loc].exit_point

	def legal_loc(self, loc):
		return 0 <= loc < self.rows * self.cols

	def get_coord(loc):
		return loc // self.cols, loc % self.cols
