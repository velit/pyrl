from pyrl.enums.colors import ColorPair
from pyrl.world.tile import Tile

class PyrlTile:
    # Name         Description                      Visible char        Memory char                Pathable Transparency
    Unknown      = Tile("nothing",                 (' ', ColorPair.Normal), (' ', ColorPair.Normal),  False,   False)
    Floor        = Tile("dungeon floor",           ('.', ColorPair.Light),  ('.', ColorPair.Gray),    True,    True)
    Black_Floor  = Tile("obisidian dungeon floor", ('.', ColorPair.Red),    ('.', ColorPair.Red),     True,    True)
    Wall         = Tile("wall",                    ('#', ColorPair.Brown),  ('#', ColorPair.Dark),    False,   False)
    Rock         = Tile("dungeon rock",            ('#', ColorPair.Dark),   ('#', ColorPair.Darkest), False,   False)
    Dynamic_Wall = Tile("game creation wall",      ('#', ColorPair.Green),  ('#', ColorPair.Green),   False,   False)
    Open_Door    = Tile("closed door",             ('+', ColorPair.Brown),  ('+', ColorPair.Brown),   False,   False)
    Closed_Door  = Tile("open door",               ('/', ColorPair.Brown),  ('/', ColorPair.Brown),   True,    True)
    Stairs_Down  = Tile("down staircase",          ('>', ColorPair.Red),    ('>', ColorPair.Normal),  True,    True)
    Stairs_Up    = Tile("up staircase",            ('<', ColorPair.Red),    ('<', ColorPair.Normal),  True,    True)
