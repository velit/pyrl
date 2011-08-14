import const.game as CG
from tile import Tile
from char import Char
from const.tiles import UNKNOWN, FLOOR, WALL, ROCK, STAIRS_UP, STAIRS_DOWN


tiles = { #TODO: tallenna jsonina ja loadaa gameen/editoriin erikseen
	UNKNOWN: Tile("You have not seen this place yet",
			Char(' '), Char(' '), False, False),
	FLOOR: Tile("Dungeon floor", Char('.'), Char('.')),
	ROCK: Tile("Dungeon rock", Char('#', "black"), Char('#', "black"),
			False, False),
	WALL: Tile("Wall", Char('#', "brown"), Char('#', "black"),
			False, False),
	STAIRS_DOWN: Tile("Down staircase", Char('>', "red"), Char('>'),
			exit_point=CG.PASSAGE_DOWN),
	STAIRS_UP: Tile("Up staircase", Char('<', "red"), Char('<'),
			exit_point=CG.PASSAGE_UP),
}


def gettile(handle, tile_dict=None):
	if tile_dict is not None and handle in tile_dict:
		return tile_dict[handle]
	elif handle in tiles:
		return tiles[handle]
	else:
		raise KeyError("Handle '{}' not in global tiles nor in '{}'".format(handle, tile_dict))
