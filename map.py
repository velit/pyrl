import random

from square import Square
from tiles import gettile, FLOOR
from const.game import PASSAGE_RANDOM


class Map:
	"""Actual map data structure used in-game containing Squares."""

	def __init__(self, map_file):
		self.rows = map_file.rows
		self.cols = map_file.cols
		self.squares = []
		self.entrance_squares = {}

		for i, k in enumerate(map_file.tilemap):
			self.squares.append(Square(gettile(k, map_file.tile_dict),
					i // self.cols, i % self.cols))

		for key, loc_ in map_file.entrance_locs.items():
			self.entrance_squares[key] = self.getsquare(loc=loc_)

	def getsquare(self, *a, **k):
		if "entrance" in k:
			if k["entrance"] == PASSAGE_RANDOM:
				return self.get_free_square()
			else:
				return self.entrance_squares[k["entrance"]]
		elif "loc" in k:
			y, x = k["loc"]
		else:
			y, x = a
		return self.squares[y*self.cols + x]

	def get_free_square(self):
		"""Randomly finds an unoccupied passable square and returns it."""
		while True:
			square = self.get_random_square()
			if square.passable():
				return square

	def get_random_square(self):
		"""Returns a random square from the Map."""
		return random.choice(self.squares)

	def legal_loc(self, loc):
		y, x = loc
		return 0 <= y < self.rows and 0 <= x < self.cols

	def legal_coord(self, y, x):
		return 0 <= y < self.rows and 0 <= x < self.cols

	def get_edge_square(self):
		#TODO: implement
		pass
