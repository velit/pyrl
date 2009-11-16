from char import Char
from io import io

class Tile:
	"""The actual floor of a square."""
	def __init__(self, name = "Unknown", ch = Char(' '), \
			passable = False, destroyable = False, see_through = False ):
		self.name = name
		self.ch = ch
		self.passable = passable
		self.destroyable = destroyable
		self.see_through = see_through

tiles = {
		"u": Tile("You have not seen this place yet", Char(' '), False, False, False),
		"f": Tile("Dungeon floor", Char('.'), True, False, True),
		"r": Tile("Dungeon rock", Char('#'), False, True, False),
		"w": Tile("Wall", Char('#', io.color["black"]), False, True, False),
		"ds": Tile("Down staircase", Char('>'), True, True, True),
		"us": Tile("Up staircase", Char('<'), True, True, True),
		}
