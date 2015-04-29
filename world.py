from __future__ import absolute_import, division, print_function, unicode_literals

from level import Level


class World(object):

    def __init__(self, world_template, visible_change_callback):
        self.visible_change_callback = visible_change_callback
        self.world_template = world_template
        self.levels = {}

    def get_level(self, world_loc):
        try:
            return self.levels[world_loc]
        except KeyError:
            level_template = self.world_template.get_level_template(world_loc)
            level_template.finalize()
            level = Level(world_loc, level_template, [self.visible_change_callback])
            self.levels[world_loc] = level
            return level

    def get_first_level_info(self):
        return self.world_template.first_level_info
