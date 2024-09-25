from __future__ import annotations

from pyrl.engine.world.world import World
from pyrl.engine.world.enums.level_key import LevelKey
from pyrl.engine.world.enums.world_point import WorldPoint
from pyrl.game_data.levels import test_level, overworld
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.game_data.pyrl_player import pyrl_player

def pyrl_world() -> World:

    world = World(pyrl_player())
    start = LevelKey("dungeon", 1)
    world.add_level(start.dungeon, test_level.get_level(world.player))

    for _ in range(99 - 1):
        world.add_level(start.dungeon)

    world.add_level(overworld.name, overworld.get_level())

    world.set_two_way_connection(
        WorldPoint(LevelKey(overworld.name, 1), overworld.OverWorldLocation.Dungeon),
        WorldPoint(start, DefaultLocation.Passage_Up))

    world.get_level(start)
    return world
