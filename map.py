import random

from square import Square
from tiles import gettile, FLOOR
from const.game import MAP_ROWS, MAP_COLS, PASSAGE_RANDOM


class Map(list):

	def __init__(self, tilemap, *args, **kwords):
		"""Actual map data structure used in-game containing Squares."""
		list.__init__(self)
		self.cols = tilemap.cols
		self.creature_squares = {}
		self.entrance_squares = {}
		for i, k in enumerate(tilemap):
			self.append(Square(gettile(k, tilemap.tile_dict), i // self.cols,
					i % self.cols))

		for key, (loc_y, loc_x) in tilemap.entrance_locs.items():
			self.entrance_squares[key] = self.getsquare(loc_y, loc_x)

	def getsquare(self, *args, **kwords):
		if "loc" in kwords:
			return self.getsquare(kwords["loc"][0], kwords["loc"][1])
		elif "entrance" in kwords:
			if kwords["entrance"] == PASSAGE_RANDOM:
				return self.get_free_square()
			else:
				return self.entrance_squares[kwords["entrance"]]
		elif "creature" in kwords:
			return self.creature_squares[kwords["creature"]]
		else:
			return self[args[0]*self.cols + args[1]]

	def get_free_square(self):
		"""Randomly finds an unoccupied passable square and returns it."""
		while True:
			square = self.get_random_square()
			if square.passable():
				return square

	def get_random_square(self):
		"""Returns a random square from the Map."""
		return random.choice(self)

	def get_edge_square(self):
		#TODO: implement
		pass


class TileMap(list):
	"""A map containing the tiles of a level."""

	def __init__(self, rows=MAP_ROWS, cols=MAP_COLS, tile=FLOOR):
		list.__init__(self, (tile for i in range(rows * cols)))
		self.rows = rows
		self.cols = cols
		self.tile_dict = {}
		self.entrance_locs = {}

	def getsquare(self, *args):
		if len(args) == 1:
			return self.entrance_locs[args[0]]
		else:
			return self[args[0] * self.cols + args[1]]

	def setsquare(self, y, x, tile):
		self[y * self.cols + x] = tile
