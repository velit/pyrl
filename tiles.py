import const.game as GAME
from tile import Tile
from char import Char
from const.tiles import UNKNOWN, FLOOR, WALL, ROCK, STAIRS_UP, STAIRS_DOWN
from const.colors import BLACK, BROWN, RED


tiles = { #TODO: tallenna jsonina ja loadaa gameen/editoriin erikseen
	UNKNOWN: Tile("You have not seen this place yet",
			Char(' '), Char(' '), False, False),
	FLOOR: Tile("dungeon floor", Char('.'), Char('.')),
	ROCK: Tile("dungeon rock", Char('#', BLACK), Char('#', BLACK),
			False, False),
	WALL: Tile("wall", Char('#', BROWN), Char('#', BLACK),
			False, False),
	STAIRS_DOWN: Tile("down staircase", Char('>', RED), Char('>'),
			exit_point=GAME.PASSAGE_DOWN),
	STAIRS_UP: Tile("up staircase", Char('<', RED), Char('<'),
			exit_point=GAME.PASSAGE_UP),
}


def gettile(handle, tile_dict=None):
	if tile_dict is not None and handle in tile_dict:
		return tile_dict[handle]
	elif handle in tiles:
		return tiles[handle]
	else:
		raise KeyError("Handle '{}' not in global tiles nor in '{}'".format(handle, tile_dict))
