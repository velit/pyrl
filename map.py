import random

from tile import tiles
from square import Square

class Map(list):
	def __init__(self, dummy):
		self.rows = dummy.rows
		self.cols = dummy.cols
		self.squares = dummy.squares
		x = self.cols #helpful alias / auttajatonttu
		for i, tilekey in enumerate(dummy):
			if tilekey in dummy.tiles:
				self.append(Square(dummy.tiles[tilekey], i / x, i % x))
			else:
				self.append(Square(tiles[tilekey], i / x, i % x))

	def getsquare(self, str_or_y, x=None):
		if isinstance(str_or_y, str):
			return self.squares[str_or_y]
		else:
			return self[str_or_y*self.cols + x]

	def get_free_tile(self):
		while True:
			tile = self.get_random_tile()
			if tile.passable():
				return tile

	def get_random_tile(self):
		return random.choice(self)
