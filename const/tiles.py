import const.game as GAME
from tile import Tile
from const.colors import *

UNKNOWN = " "
FLOOR = "."
WALL = "w"
ROCK = "#"
STAIRS_UP = "<"
STAIRS_DOWN = ">"

tiles = {
	UNKNOWN: Tile("You have not seen this place yet", (' ', NORMAL), (' ', NORMAL), False, False),
	FLOOR: Tile("dungeon floor", ('.', LIGHT), ('.', GRAY)),
	WALL: Tile("wall", ('#', BROWN), ('#', DARK), False, False),
	ROCK: Tile("dungeon rock", ('#', DARK), ('#', DARKEST), False, False),
	STAIRS_DOWN: Tile("down staircase", ('>', RED), ('>', NORMAL), exit_point=GAME.PASSAGE_DOWN),
	STAIRS_UP: Tile("up staircase", ('<', RED), ('<', NORMAL), exit_point=GAME.PASSAGE_UP),
	'+': Tile("Closed door", ('+', BROWN), ('+', BROWN), False, False),
	'/': Tile("Open door", ('/', BROWN), ('/', BROWN)),
	'o': Tile("Window", ('o', NORMAL), ('o', NORMAL), False, True),
	'=': Tile("Closet", ('=', BROWN), ('=', BROWN), False, True),
	'-': Tile("Small table", ('-', BROWN), ('-', BROWN), False, True),
	'c': Tile("Chair", ('c', DARK), ('c', DARK)),
	's': Tile("Sink", ('s', WHITE), ('s', WHITE), False, True),
	't': Tile("Toilet", ('t', WHITE), ('t', WHITE)),
	'"': Tile("Grass", ('"', GREEN), ('"', GREEN)),
}
