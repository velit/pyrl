from tile import tiles
from io import io

class Square:
	def __init__(self, tile, y, x):
		self.y = y
		self.x = x
		self.tile = tile
		self.creature = None
		self.memory_tile = tiles["u"]

	#returns true if the square is passable by creatures
	def passable(self):
		if self.creature:
			return False
		elif self.tile:
			return self.tile.passable
		else:
			return False

	def seeThrough(self):
		return self.tile.see_through

	def visit(self):
		self.memory_tile = self.tile

	def getVisibleChar(self):
		if self.creature:
			return self.creature.ch
		else:
			return self.tile.ch

	def getMemoryChar(self):
		return self.memory_tile.ch
