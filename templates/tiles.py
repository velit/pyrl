from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import const.game as GAME
import const.colors as C
from tile import Tile

UNKNOWN = " "
FLOOR = "."
BLACK_FLOOR = "b"
WALL = "w"
ROCK = "#"
STAIRS_UP = "<"
STAIRS_DOWN = ">"

tiles = {
    UNKNOWN: Tile("You have not seen this place yet", (' ', C.NORMAL), (' ', C.NORMAL), False, False),
    FLOOR: Tile("dungeon floor", ('.', C.LIGHT), ('.', C.GRAY)),
    BLACK_FLOOR: Tile("obisidian dungeon floor", ('.', C.RED), ('.', C.RED)),
    WALL: Tile("wall", ('#', C.BROWN), ('#', C.DARK), False, False),
    ROCK: Tile("dungeon rock", ('#', C.DARK), ('#', C.DARKEST), False, False),
    STAIRS_DOWN: Tile("down staircase", ('>', C.RED), ('>', C.NORMAL), exit_point=GAME.PASSAGE_DOWN),
    STAIRS_UP: Tile("up staircase", ('<', C.RED), ('<', C.NORMAL), exit_point=GAME.PASSAGE_UP),
    '+': Tile("Closed door", ('+', C.BROWN), ('+', C.BROWN), False, False),
    '/': Tile("Open door", ('/', C.BROWN), ('/', C.BROWN)),
    'o': Tile("Window", ('o', C.NORMAL), ('o', C.NORMAL), False, True),
    '=': Tile("Closet", ('=', C.BROWN), ('=', C.BROWN), False, True),
    '-': Tile("Small table", ('-', C.BROWN), ('-', C.BROWN), False, True),
    'c': Tile("Chair", ('c', C.DARK), ('c', C.DARK)),
    's': Tile("Sink", ('s', C.WHITE), ('s', C.WHITE), False, True),
    't': Tile("Toilet", ('t', C.WHITE), ('t', C.WHITE)),
    '"': Tile("Grass", ('"', C.GREEN), ('"', C.GREEN)),
}
