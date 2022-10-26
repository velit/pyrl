from __future__ import annotations

from pyrl.game_data.levels.shared_assets import construct_data, default_dims, AssetLocationDict, AssetCreatureDict, \
    AssetTileDict
from pyrl.types.color import Colors
from pyrl.types.level_gen import LevelGen
from pyrl.types.level_location import LevelLocation
from pyrl.world.level_gen_params import LevelGenParams
from pyrl.world.tile import Tile

name = "overworld"

class OverWorldLocation(LevelLocation):
    Dungeon = 1
    Village = 2

def get_level() -> LevelGenParams:
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
        '"': Tile("grassland",      ('"', Colors.Green), ('"', Colors.Green), True,  True,  move_multi=mult),
        '¨': Tile("mountains",      ('^', Colors.White), ('^', Colors.White), False, True,  move_multi=mult),
        '=': Tile("river",          ('=', Colors.Blue),  ('=', Colors.Blue),  False, False, move_multi=mult),
        'T': Tile("forest",         ('T', Colors.Green), ('T', Colors.Green), True,  True,  move_multi=mult),
        't': Tile("town",           ('*', Colors.Green), ('*', Colors.Green), True,  True,  move_multi=mult),
        '*': Tile("dungeon",        ('*', Colors.Brown), ('*', Colors.Brown), True,  True,  move_multi=mult),
        '^': Tile("high mountains", ('^', Colors.Brown), ('^', Colors.Brown), False, False, move_multi=mult),
    }
    custom_locations: AssetLocationDict = {
        '*': OverWorldLocation.Dungeon,
        't': OverWorldLocation.Village,
    }
    custom_creatures: AssetCreatureDict = {
    }
    tiles, locations, creatures = construct_data(dimensions, charstr, custom_tiles, custom_locations, custom_creatures)

    return LevelGenParams(
        dimensions=dimensions,
        area_level=0,
        tiles=tiles,
        locations=locations,
        custom_creatures=creatures,
        initial_creature_spawns=False,
        ongoing_creature_spawns=False,
        generation_type=LevelGen.NoGeneration,
    )
