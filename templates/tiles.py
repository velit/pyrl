from __future__ import absolute_import, division, print_function, unicode_literals

import const.game as GAME
import const.colors as COL
from tile import Tile

UNKNOWN = " "
FLOOR = "."
BLACK_FLOOR = "b"
WALL = "w"
ROCK = "r"
DYNAMIC_WALL = "#"
STAIRS_UP = "<"
STAIRS_DOWN = ">"

tiles = {
    UNKNOWN: Tile("You have not seen this place yet", (' ', COL.NORMAL), (' ', COL.NORMAL), False, False),
    FLOOR: Tile("dungeon floor", ('.', COL.LIGHT), ('.', COL.GRAY)),
    BLACK_FLOOR: Tile("obisidian dungeon floor", ('.', COL.RED), ('.', COL.RED)),
    WALL: Tile("wall", ('#', COL.BROWN), ('#', COL.DARK), False, False),
    ROCK: Tile("dungeon rock", ('#', COL.DARK), ('#', COL.DARKEST), False, False),
    STAIRS_DOWN: Tile("down staircase", ('>', COL.RED), ('>', COL.NORMAL), exit_point=GAME.PASSAGE_DOWN),
    STAIRS_UP: Tile("up staircase", ('<', COL.RED), ('<', COL.NORMAL), exit_point=GAME.PASSAGE_UP),
    '+': Tile("Closed door", ('+', COL.BROWN), ('+', COL.BROWN), False, False),
    '/': Tile("Open door", ('/', COL.BROWN), ('/', COL.BROWN)),
    'o': Tile("Window", ('o', COL.NORMAL), ('o', COL.NORMAL), False, True),
    '=': Tile("Closet", ('=', COL.BROWN), ('=', COL.BROWN), False, True),
    '-': Tile("Small table", ('-', COL.BROWN), ('-', COL.BROWN), False, True),
    'c': Tile("Chair", ('c', COL.DARK), ('c', COL.DARK)),
    's': Tile("Sink", ('s', COL.WHITE), ('s', COL.WHITE), False, True),
    't': Tile("Toilet", ('t', COL.WHITE), ('t', COL.WHITE)),
    '"': Tile("Grass", ('"', COL.GREEN), ('"', COL.GREEN)),
}
