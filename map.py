from __future__ import division

import random

from square import Square as S

class Map(list):
	def __init__(self, y, x, tile=None, seq=None):
		if tile:
			list.__init__(self, (S(tile, i // x, i % x) for i in range(y * x)))
		else:
			list.__init__(self, (S(tile, i // x, i % x) for (i, tile) in
					enumerate(seq)))
		self.rows = y
		self.cols = x
		self.squares = {}

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
