import random

from tile import tiles
from square import Square

class Map(list):
	def __init__(self, tilemap):
		"""Actual map data structure used in-game containing Squares."""
		self.rows = tilemap.rows
		self.cols = tilemap.cols
		self.squares = {}
		x = self.cols #auttajatonttu
		for i, tilekey in enumerate(tilemap):
			if tilekey in tilemap.tiles:
				self.append(Square(tilemap.tiles[tilekey], i / x, i % x))
			else:
				self.append(Square(tiles[tilekey], i / x, i % x))
		for key, value in tilemap.squares.iteritems():
			self.squares[key] = self.getsquare(*value)

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
