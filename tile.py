from char import Char
from colors import color
from cPickle import load

class Tile(object):
	"""The actual floor of a square."""
	def __init__(self, name = "Unknown", visible_ch = Char(' '), memory_ch = Char(' '),
			passable = False, destroyable = False, see_through = False ):
		self.name = name
		self.visible_ch = visible_ch
		self.memory_ch = memory_ch
		self.passable = passable
		self.destroyable = destroyable
		self.see_through = see_through

#tiles = {
#		"u": Tile("You have not seen this place yet", Char(' '), Char(' '), False, False, False),
#		"f": Tile("Dungeon floor", Char('.'), Char('.'), True, False, True),
#		"r": Tile("Dungeon rock", Char('#'), Char('#'), False, True, False),
#		"w": Tile("Wall", Char('#', color["brown"]), Char('#', color["black"]), False, True, False),
#		"ds": Tile("Down staircase", Char('>'), Char('>'), True, True, True),
#		"us": Tile("Up staircase", Char('<'), Char('<'), True, True, True),
#		}
