from __future__ import absolute_import, division, print_function, unicode_literals

from enums.colors import Pair
import const.game as GAME
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
    UNKNOWN: Tile("You have not seen this place yet", (' ', Pair.Normal), (' ', Pair.Normal), False, False),
    FLOOR: Tile("dungeon floor", ('.', Pair.Light), ('.', Pair.Gray)),
    BLACK_FLOOR: Tile("obisidian dungeon floor", ('.', Pair.Red), ('.', Pair.Red)),
    WALL: Tile("wall", ('#', Pair.Brown), ('#', Pair.Dark), False, False),
    ROCK: Tile("dungeon rock", ('#', Pair.Dark), ('#', Pair.Darkest), False, False),
    STAIRS_DOWN: Tile("down staircase", ('>', Pair.Red), ('>', Pair.Normal), exit_point=GAME.PASSAGE_DOWN),
    STAIRS_UP: Tile("up staircase", ('<', Pair.Red), ('<', Pair.Normal), exit_point=GAME.PASSAGE_UP),
    '+': Tile("Closed door", ('+', Pair.Brown), ('+', Pair.Brown), False, False),
    '/': Tile("Open door", ('/', Pair.Brown), ('/', Pair.Brown)),
    'o': Tile("Window", ('o', Pair.Normal), ('o', Pair.Normal), False, True),
    '=': Tile("Closet", ('=', Pair.Brown), ('=', Pair.Brown), False, True),
    '-': Tile("Small table", ('-', Pair.Brown), ('-', Pair.Brown), False, True),
    'c': Tile("Chair", ('c', Pair.Dark), ('c', Pair.Dark)),
    's': Tile("Sink", ('s', Pair.White), ('s', Pair.White), False, True),
    't': Tile("Toilet", ('t', Pair.White), ('t', Pair.White)),
    '"': Tile("Grass", ('"', Pair.Green), ('"', Pair.Green)),
}
