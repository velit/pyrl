from tile import tiles
from io import io

opti = True

class Square(object):
	"""A cell that is a part of a level."""

	if opti: __slots__ = ("x", "y", "tile", "creature", "memory_tile")

	def __init__(self, tile, y, x):
		self.y = y
		self.x = x
		self.tile = tile
		self.creature = None
		self.memory_tile = tiles["u"]

	if opti:
		def __getstate__(self):
			return self.y, self.x, self.tile, self.creature, self.memory_tile
	if opti:
		def __setstate__(self, state):
			self.y, self.x, self.tile, self.creature, self.memory_tile = state

	#returns true if the square is passable by creatures
	def passable(self):
		if self.creature:
			return False
		elif self.tile:
			return self.tile.passable
		else:
			return False

	def tile_passable(self):
		if self.tile:
			return self.tile.passable

	def seeThrough(self):
		return self.tile.see_through

	def visit(self):
		self.memory_tile = self.tile

	def getVisibleChar(self):
		if self.creature:
			return self.creature.ch
		else:
			return self.tile.visible_ch

	def getMemoryChar(self):
		return self.memory_tile.memory_ch
