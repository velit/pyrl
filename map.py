import random

from square import Square
from tile import gettile

from const.tiles import FLOOR

class Map(list):
	def __init__(self, tilemap):
		"""Actual map data structure used in-game containing Squares."""
		self.rows = tilemap.rows
		self.cols = tilemap.cols
		self.squares = {}
		x = self.cols #auttajatonttu
		for i, tilekey in enumerate(tilemap):
			self.append(Square(gettile(tilemap,tilekey), i // x, i % x))

		for key, (loc_y, loc_x) in tilemap.squares.items():
			self.squares[key] = self.getsquare(loc_y, loc_x)

	def getsquare(self, y, x=None):
		"""Returns a square according to parameters.

		With one parameter returns a square according to key.
		With two parameters returns according to coordinates.
		"""
		if x is not None:
			return self[y*self.cols + x]
		else:
			return self.squares[y]

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
		self.passageway_locs = {}

	def getsquare(self, *args):
		if len(args) == 2:
			y, x = args
			return self[y*self.cols + x]
		else:
			return self.squares[args[0]]

	def setsquare(self, y, x, tile):
		self[y*self.cols + x] = tile
