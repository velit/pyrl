import random

from square import Square
from tiles import gettile, FLOOR
from const.game import PASSAGE_RANDOM


class Map:
	"""Actual map data structure used in-game containing Squares."""

	def __init__(self, template):
		self.rows = template.rows
		self.cols = template.cols
		self.squares = []
		self.entrance_squares = {}

		for i, k in enumerate(template.tilemap):
			self.squares.append(Square(gettile(k, template.tile_dict),
					i // self.cols, i % self.cols))

		for key, loc_ in template.entrance_locs.items():
			self.entrance_squares[key] = self.getsquare(loc=loc_)

	def getsquare(self, *args, **kwords):
		if "loc" in kwords:
			return self.squares[kwords["loc"][0]*self.cols + kwords["loc"][1]]
		elif "entrance" in kwords:
			if kwords["entrance"] == PASSAGE_RANDOM:
				return self.get_free_square()
			else:
				return self.entrance_squares[kwords["entrance"]]
		else:
			return self.squares[args[0]*self.cols + args[1]]

	def get_free_square(self):
		"""Randomly finds an unoccupied passable square and returns it."""
		while True:
			square = self.get_random_square()
			if square.passable():
				return square

	def get_random_square(self):
		"""Returns a random square from the Map."""
		return random.choice(self.squares)

	def legal_loc(self, y, x):
		return 0 <= y < self.rows and 0 <= x < self.cols

	def get_edge_square(self):
		#TODO: implement
		pass
