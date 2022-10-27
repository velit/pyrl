from __future__ import annotations

from pyrl.types.glyphs import Colors
from pyrl.world.tile import Tile

class PyrlTiles:
    # Name         Description                      Visible glyph         Memory glyph        Pathable Transparency
    Unknown      = Tile("nothing",                 (' ', Colors.Normal), (' ', Colors.Normal),  False, False)
    Floor        = Tile("dungeon floor",           ('.', Colors.Light),  ('.', Colors.Gray),    True,  True)
    Black_Floor  = Tile("obisidian dungeon floor", ('.', Colors.Red),    ('.', Colors.Red),     True,  True)
    Wall         = Tile("wall",                    ('#', Colors.Brown),  ('#', Colors.Dark),    False, False)
    Rock         = Tile("dungeon rock",            ('#', Colors.Dark),   ('#', Colors.Darkest), False, False)
    Dynamic_Wall = Tile("game creation wall",      ('#', Colors.Green),  ('#', Colors.Green),   False, False)
    Open_Door    = Tile("closed door",             ('+', Colors.Brown),  ('+', Colors.Brown),   False, False)
    Closed_Door  = Tile("open door",               ('/', Colors.Brown),  ('/', Colors.Brown),   True,  True)
    Stairs_Down  = Tile("down staircase",          ('>', Colors.Red),    ('>', Colors.Normal),  True,  True)
    Stairs_Up    = Tile("up staircase",            ('<', Colors.Red),    ('<', Colors.Normal),  True,  True)
