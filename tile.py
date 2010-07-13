from char import Char

class Tile(object):
	"""The actual floor of a square."""

	def __init__(self, name="name", visible=Char(), mem=Char(), passable=False,
				destroyable=False, see_through=False, movement_cost=1000):
		self.name = name
		self.ch_visible = visible
		self.ch_memory = mem
		self.passable = passable
		self.destroyable = destroyable
		self.see_through = see_through
		self.movement_cost = movement_cost

#tiles = {
#	"u": Tile("You have not seen this place yet",
#				Char(' '), Char(' '), False, False, False),
#	"f": Tile("Dungeon floor", Char('.'), Char('.'), True, False, True),
#	"r": Tile("Dungeon rock", Char('#', color["black"]),
#				Char('#', color["black"]), False, True, False),
#	"w": Tile("Wall", Char('#', color["brown"]), Char('#', color["black"]),
#				False, True, False),
#	"ds": Tile("Down staircase", Char('>'), Char('>'), True, True, True),
#	"us": Tile("Up staircase", Char('<'), Char('<'), True, True, True),
#}
