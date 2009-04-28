from char import Char

class Tile:
	"Tile (floor) part of a square."
	def __init__(self, name = "Unknown", ch = Char(' '), \
			passable = False, destroyable = False, see_through = False ):
		self.name = name
		self.ch = ch
		self.passable = passable
		self.destroyable = destroyable
		self.see_through = see_through
