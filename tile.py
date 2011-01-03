from char import Char
from constants import PASSAGE_DOWN, PASSAGE_UP

class Tile(object):
	"""The actual floor of a square."""

	def __init__(self, name="floor", visible=Char(), mem=Char(), passable=True,
				see_through=True, movement_cost=1000):
		self.name = name
		self.ch_visible = visible
		self.ch_memory = mem
		self.passable = passable
		self.see_through = see_through
		self.movement_cost = movement_cost


class PassageTile(Tile):
	"""A tile that signifies a passageway exists."""

	def __init__(self, passage=None, *args, **kwargs):
		self.passage = passage
		super(PassageTile, self).__init__(*args, **kwargs)

tiles = {
	"u": Tile("You have not seen this place yet",
			Char(' '), Char(' '), False, False),
	"f": Tile("Dungeon floor", Char('.'), Char('.'), True, True),
	"r": Tile("Dungeon rock", Char('#', "black"),
			Char('#', "black"), False, False),
	"w": Tile("Wall", Char('#', "brown"), Char('#', "black"),
			False, False),
	"ds": PassageTile(PASSAGE_DOWN, "Down staircase",
			Char('>', "red"), Char('>'), True, True),
	"us": PassageTile(PASSAGE_UP, "Up staircase",
			Char('<', "red"), Char('<'), True, True),
}
