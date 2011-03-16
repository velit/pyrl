from char import Char
from const.tiles import *

class Tile(object):
	"""The actual floor of a square."""
	def __init__(self, name="floor", visible=Char(), mem=Char(), passable=True,
				see_through=True, movement_cost=1000, passageway=False):
		self.name = name
		self.ch_visible = visible
		self.ch_memory = mem
		self.passable = passable
		self.see_through = see_through
		self.movement_cost = movement_cost
		self.passageway = passageway

tiles = { #TODO: tallenna jsonina ja loadaa gameen/editoriin erikseen
	UNKNOWN: Tile("You have not seen this place yet",
			Char(' '), Char(' '), False, False),
	FLOOR: Tile("Dungeon floor", Char('.'), Char('.')),
	ROCK: Tile("Dungeon rock", Char('#', "black"), Char('#', "black"),
			False, False),
	WALL: Tile("Wall", Char('#', "brown"), Char('#', "black"),
			False, False),
	STAIRS_DOWN: Tile("Down staircase", Char('>', "red"), Char('>'),
			passageway=PASSAGE_DOWN),
	STAIRS_UP: Tile("Up staircase", Char('<', "red"), Char('<'),
			passageway=PASSAGE_UP),
}

def gettile(tile_dict, handle):
	if handle in tiles:
		return tiles[handle]
	elif handle in tile_dict:
		return tile_dict[handle]
	else:
		raise KeyError("Handle '{}' not in global tiles or '{}'".format(handle,
			tile_dict))
