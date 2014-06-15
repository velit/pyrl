from __future__ import absolute_import, division, print_function, unicode_literals

from level import Level


class World(object):

    def __init__(self, world_template):
        self.world_template = world_template
        self.levels = {}

    def get_level(self, world_loc):
        try:
            return self.levels[world_loc]
        except KeyError:
            level = Level(world_loc, self.world_template.get_level_template(world_loc))
            self.levels[world_loc] = level
            return level
