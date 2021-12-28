from __future__ import annotations

from pyrl.creature.creature import Creature
from pyrl.types.char import Letter
from pyrl.types.color import ColorPairs
from pyrl.types.level_gen import LevelGen
from pyrl.types.level_location import LevelLocation
from pyrl.game_data.levels.shared_assets import construct_data, default_dims, AssetLocationDict, AssetCreatureDict, \
    AssetTileDict
from pyrl.world.level import Level
from pyrl.world.tile import Tile

name = "overworld"

class OverWorldLocation(LevelLocation):
    Dungeon = 1
    Village = 2

def get_level() -> Level:
    dimensions = default_dims
    charstr = (
        '^^^^^^^^¨=¨¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^¨¨=¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^¨¨t=¨¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^¨¨....¨¨¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^¨.""""T"¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^¨¨.TT"T""¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^¨*.TT""""¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^¨¨.""T"""¨¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^¨"""""""¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^¨¨¨¨¨¨¨¨¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^¨¨^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
    )

    # Overworld movement multiplier
    mult = default_dims.min
    custom_tiles: AssetTileDict = {
        '"': Tile("grassland",      ('"', ColorPairs.Green), ('"', ColorPairs.Green), True,  True,  move_multi=mult),
        '¨': Tile("mountains",      ('^', ColorPairs.White), ('^', ColorPairs.White), False, True,  move_multi=mult),
        '=': Tile("river",          ('=', ColorPairs.Blue),  ('=', ColorPairs.Blue),  False, False, move_multi=mult),
        'T': Tile("forest",         ('T', ColorPairs.Green), ('T', ColorPairs.Green), True,  True,  move_multi=mult),
        't': Tile("town",           ('*', ColorPairs.Green), ('*', ColorPairs.Green), True,  True,  move_multi=mult),
        '*': Tile("dungeon",        ('*', ColorPairs.Brown), ('*', ColorPairs.Brown), True,  True,  move_multi=mult),
        '^': Tile("high mountains", ('^', ColorPairs.Brown), ('^', ColorPairs.Brown), False, False, move_multi=mult),
    }
    custom_locations: AssetLocationDict = {
        '*': OverWorldLocation.Dungeon,
        't': OverWorldLocation.Village,
    }
    custom_creatures: AssetCreatureDict = {
    }
    tiles, locations, creatures = construct_data(dimensions, charstr, custom_tiles, custom_locations, custom_creatures)

    return Level(
        danger_level=1,
        generation_type=LevelGen.NoGeneration,
        tiles=tiles,
        locations=locations,
        custom_creatures=creatures,
        creature_spawning_enabled=False,
    )
