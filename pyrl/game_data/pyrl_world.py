from __future__ import annotations

from pyrl.game_data.levels import test_level, overworld
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.game_data.player import Player
from pyrl.world.world import World, LevelKey, WorldPoint

def get_world():

    world = World(Player())
    start = LevelKey("dungeon", 1)
    world.add_level(start.dungeon, test_level.get_level(world.player))

    for x in range(99 - 1):
        world.add_level(start.dungeon)

    world.add_level(overworld.name, overworld.get_level())

    world.set_two_way_connection(
        WorldPoint(LevelKey(overworld.name, 1), overworld.OverWorldLocation.Dungeon),
        WorldPoint(start, DefaultLocation.Passage_Up))

    world.get_level(start)
    return world
