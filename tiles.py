import const.game as GAME
from tile import Tile
from char import Char
from const.tiles import UNKNOWN, FLOOR, WALL, ROCK, STAIRS_UP, STAIRS_DOWN
from const.colors import BLACK, BROWN, RED


tiles = { #TODO: tallenna jsonina ja loadaa gameen/editoriin erikseen
	UNKNOWN: Tile(u"You have not seen this place yet",
			Char(u' '), Char(u' '), False, False),
	FLOOR: Tile(u"dungeon floor", Char(u'.'), Char(u'.')),
	ROCK: Tile(u"dungeon rock", Char(u'#', BLACK), Char(u'#', BLACK),
			False, False),
	WALL: Tile(u"wall", Char(u'#', BROWN), Char(u'#', BLACK),
			False, False),
	STAIRS_DOWN: Tile(u"down staircase", Char(u'>', RED), Char(u'>'),
			exit_point=GAME.PASSAGE_DOWN),
	STAIRS_UP: Tile(u"up staircase", Char(u'<', RED), Char(u'<'),
			exit_point=GAME.PASSAGE_UP),
}


def gettile(handle, tile_dict=None):
	if tile_dict is not None and handle in tile_dict:
		return tile_dict[handle]
	elif handle in tiles:
		return tiles[handle]
	else:
		raise KeyError(u"Handle '{}' not in global tiles nor in '{}'".format(handle, tile_dict))
