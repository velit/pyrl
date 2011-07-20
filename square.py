from const.game import OPTIMIZATION


class Square:
	"""A cell, is a part of a level."""

	if OPTIMIZATION:
		__slots__ = ("tile", "creature")

	def __init__(self, tile):
		self.tile = tile
		self.creature = None

	if OPTIMIZATION:
		def __getstate__(self):
			return self.tile, self.creature

	if OPTIMIZATION:
		def __setstate__(self, state):
			self.tile, self.creature = state

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

	def get_visible_char_data(self, color_shift=""):
		if self.creature:
			return (self.creature.ch.symbol, self.creature.ch.color + color_shift)
		else:
			return (self.tile.ch_visible.symbol, self.tile.ch_visible.color + color_shift)

	def get_memory_char_data(self, color_shift=""):
		return (self.tile.ch_memory.symbol,
				self.tile.ch_memory.color + color_shift)

	def isexit(self):
		return self.tile.exit_point is not None

	def getexit(self):
		return self.tile.exit_point
