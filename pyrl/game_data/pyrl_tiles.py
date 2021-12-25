from __future__ import annotations

from pyrl.types.color import ColorPairs
from pyrl.world.tile import Tile

class PyrlTiles:
    # Name         Description                      Visible char        Memory char                Pathable Transparency
    Unknown      = Tile("nothing",                 (' ', ColorPairs.Normal), (' ', ColorPairs.Normal),  False,   False)
    Floor        = Tile("dungeon floor",           ('.', ColorPairs.Light),  ('.', ColorPairs.Gray),    True,    True)
    Black_Floor  = Tile("obisidian dungeon floor", ('.', ColorPairs.Red),    ('.', ColorPairs.Red),     True,    True)
    Wall         = Tile("wall",                    ('#', ColorPairs.Brown),  ('#', ColorPairs.Dark),    False,   False)
    Rock         = Tile("dungeon rock",            ('#', ColorPairs.Dark),   ('#', ColorPairs.Darkest), False,   False)
    Dynamic_Wall = Tile("game creation wall",      ('#', ColorPairs.Green),  ('#', ColorPairs.Green),   False,   False)
    Open_Door    = Tile("closed door",             ('+', ColorPairs.Brown),  ('+', ColorPairs.Brown),   False,   False)
    Closed_Door  = Tile("open door",               ('/', ColorPairs.Brown),  ('/', ColorPairs.Brown),   True,    True)
    Stairs_Down  = Tile("down staircase",          ('>', ColorPairs.Red),    ('>', ColorPairs.Normal),  True,    True)
    Stairs_Up    = Tile("up staircase",            ('<', ColorPairs.Red),    ('<', ColorPairs.Normal),  True,    True)
