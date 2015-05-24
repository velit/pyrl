from __future__ import absolute_import, division, print_function, unicode_literals

from world import World
from game_data.levels import test_level


def get_world():

    world = World()
    start_dungeon = "dungeon"
    world.start_level = (start_dungeon, 1)
    world.add_level_template(start_dungeon, test_level.get_template(world))
    # Lazy initialization

    for x in range(99 - 1):
        world.add_level_template(start_dungeon)

    return world
