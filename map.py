import random

from square import Square
from tiles import gettile, FLOOR

class Map(list):
	def __init__(self, tilemap):
		"""Actual map data structure used in-game containing Squares."""
		self.rows = tilemap.rows
		self.cols = tilemap.cols
		self.entrance_squares = {}
		for i, tilekey in enumerate(tilemap):
			self.append(Square(gettile(tilekey, tilemap.tiles),
					i // self.cols, i % self.cols))

		for key, (loc_y, loc_x) in tilemap.entrance_locs.items():
			self.entrance_squares[key] = self.getsquare(loc_y, loc_x)

	def getsquare(self, *args):
		"""Returns a square according to parameters.

		With one parameter returns a square according to key.
		With two parameters returns according to coordinates.
		"""
		if len(args) == 1:
			return self.entrance_squares[args[0]]
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

class TileMap(list):
	"""A map containing the tiles of a level."""
	def __init__(self, rows, cols, tile=FLOOR):
		list.__init__(self, (tile for i in range(rows*cols)))
		self.rows = rows
		self.cols = cols
		self.tile_dict = {}
		self.entrance_locs = {}

	def getsquare(self, *args):
		if len(args) == 1:
			return self.entrance_locs[args[0]]
		else:
			return self[args[0]*self.cols + args[1]]

	def setsquare(self, y, x, tile):
		self[y*self.cols + x] = tile
