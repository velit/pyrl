import const.game as GAME
from tile import Tile
from char import Char
from const.colors import DARK, BROWN, RED, WHITE, GREEN

UNKNOWN = " "
FLOOR = "."
WALL = "#"
ROCK = "r"
STAIRS_UP = "<"
STAIRS_DOWN = ">"

tiles = {
	UNKNOWN: Tile("You have not seen this place yet", Char(' '), Char(' '), False, False),
	FLOOR: Tile("dungeon floor", Char('.'), Char('.')),
	ROCK: Tile("dungeon rock", Char('#', DARK), Char('#', DARK), False, False),
	WALL: Tile("wall", Char('#', BROWN), Char('#', DARK), False, False),
	STAIRS_DOWN: Tile("down staircase", Char('>', RED), Char('>'), exit_point=GAME.PASSAGE_DOWN),
	STAIRS_UP: Tile("up staircase", Char('<', RED), Char('<'), exit_point=GAME.PASSAGE_UP),
	'+': Tile("Closed door", Char('+', BROWN), Char('+', BROWN), False, False),
	'/': Tile("Open door", Char('/', BROWN), Char('/', BROWN), True, True),
	'o': Tile("Window", Char('o'), Char('o'), False, True),
	'=': Tile("Closet", Char('=', BROWN), Char('=', BROWN), False, True),
	'-': Tile("Small table", Char('-', BROWN), Char('-', BROWN), False, True),
	'c': Tile("Chair", Char('c', DARK), Char('c', DARK), True, True),
	's': Tile("Sink", Char('s', WHITE), Char('s', WHITE), False, True),
	't': Tile("Toilet", Char('t', WHITE), Char('t', WHITE), True, True),
	'"': Tile("Grass", Char('"', GREEN), Char('"', GREEN), True, True),
}
