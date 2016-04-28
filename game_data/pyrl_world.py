from game_data.levels import test_level, overworld
from game_data.player import Player
from world.level import LevelLocation
from world.world import World, LevelKey, WorldPoint


def get_world():

    world = World(Player())
    start = LevelKey("dungeon", 1)
    world.add_level_template(start.dungeon, test_level.get_template(world.player))

    for x in range(99 - 1):
        world.add_level_template(start.dungeon)

    world.add_level_template(overworld.name, overworld.get_template())

    world.set_two_way_connection(
        WorldPoint(LevelKey(overworld.name, 1), overworld.OverWorldLocation.Dungeon),
        WorldPoint(start, LevelLocation.Passage_Up))

    world.get_level(start)
    return world
