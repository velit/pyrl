from tiles import gettile, UNKNOWN
from const.game import OPTIMIZATION


class Square():
	"""A cell that is a part of a level."""

	if OPTIMIZATION:
		__slots__ = ("x", "y", "tile", "creature", "memory_tile")

	def __init__(self, tile, y, x):
		self.y = y
		self.x = x
		self.tile = tile
		self.creature = None
		self.memory_tile = gettile(UNKNOWN)

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

	def tile_passable(self):
		if self.tile:
			return self.tile.passable
		else:
			return False

	def see_through(self):
		return self.tile.see_through

	def visit(self):
		self.memory_tile = self.tile

	def get_visible_char_data(self, color_shift=""):
		if self.creature:
			return (self.creature.ch.symbol, self.creature.ch.color +
					color_shift)
		else:
			return (self.tile.ch_visible.symbol, self.tile.ch_visible.color +
					color_shift)

	def get_memory_char_data(self, color_shift=""):
		return (self.memory_tile.ch_memory.symbol,
				self.memory_tile.ch_memory.color + color_shift)

	def isexit(self):
		return self.tile.exit_point is not None

	def getexit(self):
		return self.tile.exit_point
