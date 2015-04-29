from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum

from enums.colors import Pair
from enums.level_locations import LevelLocation
from tile import Tile


class TileImpl(Enum):
    #name             Description                 Visible char        Memory char          Passable Transparency
    Unknown      = Tile("nothing",                 (' ', Pair.Normal), (' ', Pair.Normal),  False,   False,                       )
    Floor        = Tile("dungeon floor",           ('.', Pair.Light),  ('.', Pair.Gray),    True,    True,                        )
    Black_Floor  = Tile("obisidian dungeon floor", ('.', Pair.Red),    ('.', Pair.Red),     True,    True,                        )
    Wall         = Tile("wall",                    ('#', Pair.Brown),  ('#', Pair.Dark),    False,   False,                       )
    Rock         = Tile("dungeon rock",            ('#', Pair.Dark),   ('#', Pair.Darkest), False,   False,                       )
    Dynamic_Wall = Tile("game creation wall",      ('#', Pair.Green),  ('#', Pair.Green),   False,   False,                       )
    Open_Door    = Tile("closed door",             ('+', Pair.Brown),  ('+', Pair.Brown),   False,   False,                       )
    Closed_Door  = Tile("open door",               ('/', Pair.Brown),  ('/', Pair.Brown),   True,    True,                        )
    Grass        = Tile("grass",                   ('"', Pair.Green),  ('"', Pair.Green),   True,    True,                        )
    Stairs_Down  = Tile("down staircase",          ('>', Pair.Red),    ('>', Pair.Normal),  exit_point=LevelLocation.Passage_Down )
    Stairs_Up    = Tile("up staircase",            ('<', Pair.Red),    ('<', Pair.Normal),  exit_point=LevelLocation.Passage_Up   )