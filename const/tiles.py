import const.game as GAME
from tile import Tile
from char import Char
from const.colors import DARK, BROWN, RED, WHITE, GREEN

UNKNOWN = " "
FLOOR = "."
WALL = "w"
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
	'#': Tile("House wall", Char('#', WHITE), Char('#', WHITE), False, False),
	'+': Tile("Closed door", Char('+', BROWN), Char('+', BROWN), False, False),
	'/': Tile("Open door", Char('/', BROWN), Char('/', BROWN), True, True),
	'o': Tile("Window", Char('o'), Char('o'), False, True),
	'=': Tile("Closet", Char('=', BROWN), Char('=', BROWN), False, True),
	'-': Tile("Small table", Char('-', BROWN), Char('-', BROWN), False, True),
	'c': Tile("Chair", Char('c', DARK), Char('c', DARK), True, True),
	's': Tile("Sink", Char('s', WHITE), Char('s', WHITE), False, True),
	'p': Tile("Piano", Char('p', DARK), Char('p', DARK), False, True),
	't': Tile("Toilet", Char('t', WHITE), Char('t', WHITE), True, True),
	'g': Tile("Grass", Char('"', GREEN), Char('"', GREEN), True, True),
	'^': Tile("Car trunk", Char('^', DARK), Char('^', DARK), False, True),
	'|': Tile("Car plate", Char('|', DARK), Char('|', DARK), False, True),
	'T': Tile("Letter", Char('T', DARK), Char('T', DARK), False, True),
	'A': Tile("Letter", Char('A', DARK), Char('A', DARK), False, True),
	'B': Tile("Letter", Char('B', DARK), Char('B', DARK), False, True),
	'L': Tile("Letter", Char('L', DARK), Char('L', DARK), False, True),
	'E': Tile("Letter", Char('E', DARK), Char('E', DARK), False, True),
	'D': Tile("Letter", Char('D', DARK), Char('D', DARK), False, True),
	'V': Tile("Letter", Char('V', DARK), Char('V', DARK), False, True),
	'C': Tile("Letter", Char('C', DARK), Char('C', DARK), False, True),
	'U': Tile("Letter", Char('U', DARK), Char('U', DARK), False, True),
	'S': Tile("Letter", Char('S', DARK), Char('S', DARK), False, True),
	'O': Tile("Letter", Char('O', DARK), Char('O', DARK), False, True),
	'F': Tile("Letter", Char('F', DARK), Char('F', DARK), False, True),
	'R': Tile("Letter", Char('R', DARK), Char('R', DARK), False, True),
}
