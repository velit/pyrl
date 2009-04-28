from char import Char

class Tile:
	"""Tile (floor) part of a square."""
	def __init__(self, name = "Dungeon floor", ch = Char('.'), \
			passable = True, destroyable = False, see_through = True ):
		self.name = name
		self.ch = ch
		self.passable = passable
		self.destroyable = destroyable
		self.see_through = see_through
