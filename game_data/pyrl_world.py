from __future__ import absolute_import, division, print_function, unicode_literals

from world import World
from game_data.levels import test_level, overworld
from game_data.player import Player
from level import LevelLocation


def get_world():

    world = World(Player())
    start_dungeon = "dungeon"
    world.start_level = (start_dungeon, 1)
    world.add_level_template(start_dungeon, test_level.get_template(world.player))

    for x in range(99 - 1):
        world.add_level_template(start_dungeon)

    world.add_level_template("overworld", overworld.get_template())

    world.add_two_way_connection((("overworld", 1), overworld.OverWorldLocation.Dungeon),
                                 ((("dungeon"), 1), LevelLocation.Passage_Up))

    return world
