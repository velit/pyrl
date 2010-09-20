from tile import tiles
from io import io
from constants import OPTIMIZATION
from colors import d

class Square(object):
	"""A cell that is a part of a level."""

	if OPTIMIZATION: __slots__ = ("x", "y", "tile", "creature", "memory_tile")

	def __init__(self, tile, y, x):
		self.y = y
		self.x = x
		self.tile = tile
		self.creature = None
		self.memory_tile = tiles["u"]

	if OPTIMIZATION:
		def __getstate__(self):
			return self.y, self.x, self.tile, self.creature, self.memory_tile
	if OPTIMIZATION:
		def __setstate__(self, state):
			self.y, self.x, self.tile, self.creature, self.memory_tile = state

	def getloc(self):
		return self.y, self.x

	def passable(self):
		if self.creature:
			return False
		elif self.tile:
			return self.tile.passable
		else:
			return False

	# without regard for the passability of the square, is the underlying tile
	def tile_passable(self):
		if self.tile:
			return self.tile.passable
		else:
			return False

	def see_through(self):
		return self.tile.see_through

	def visit(self):
		self.memory_tile = self.tile

	def get_visible_data(self, color_shift="normal", coords=True):
		if coords:
			if self.creature:
				return (self.y, self.x, self.creature.ch.symbol,
						d[self.creature.ch.color] | d[color_shift])
			else:
				return (self.y, self.x, self.tile.ch_visible.symbol,
						d[self.tile.ch_visible.color] | d[color_shift])
		else:
			if self.creature:
				return (self.creature.ch.symbol,
						d[self.creature.ch.color] | d[color_shift])
			else:
				return (self.tile.ch_visible.symbol,
						d[self.tile.ch_visible.color] | d[color_shift])

	def get_memory_data(self, color_shift="normal", coords=True):
		if coords:
			return (self.y, self.x, self.memory_tile.ch_memory.symbol,
					d[self.memory_tile.ch_memory.color] | d[color_shift])
		else:
			return (self.memory_tile.ch_memory.symbol,
					d[self.memory_tile.ch_memory.color] | d[color_shift])

	def get_visible_char(self):
		if self.creature:
			return self.creature.ch
		else:
			return self.tile.ch_visible
