import random

class DummyMap(list):
	def __init__(self, y, x, t="f"):
		self.tiles = {}
		list.__init__(self, (t for x in range(y*x)))
		self.rows = y
		self.cols = x
		self.squares = {}

	def getsquare(self, y, x):
		return self[y*self.cols + x]
