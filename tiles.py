import const.game as GAME
from tile import Tile
from char import Char
from const.tiles import UNKNOWN, FLOOR, WALL, ROCK, STAIRS_UP, STAIRS_DOWN
from const.colors import BLACK, BROWN, RED, WHITE


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
	'#': Tile("House wall", Char('#', WHITE), Char('#', WHITE), False, False),
	'+': Tile("Closed door", Char('+', BROWN), Char('+', BROWN), False, False),
	'/': Tile("Open door", Char('/', BROWN), Char('/', BROWN), True, True),
	'o': Tile("Window", Char('o'), Char('o'), True, False),
	'=': Tile("Closet", Char('=', BROWN), Char('=', BROWN), False, True),
	'-': Tile("Small table", Char('-', BROWN), Char('-', BROWN), False, True),
	'-': Tile("Chair", Char('c', BLACK), Char('c', BLACK), True, True),
	'T': Tile("T", Char('T', BLACK), Char('T', BLACK), True, False),
	'T': Tile("T", Char('T', BLACK), Char('T', BLACK), True, False),
	'T': Tile("T", Char('T', BLACK), Char('T', BLACK), True, False),
	'T': Tile("T", Char('T', BLACK), Char('T', BLACK), True, False),
}


def gettile(handle, tile_dict=None):
	if tile_dict is not None and handle in tile_dict:
		return tile_dict[handle]
	elif handle in tiles:
		return tiles[handle]
	else:
		raise KeyError("Handle '{}' not in global tiles nor in '{}'".format(handle, tile_dict))
