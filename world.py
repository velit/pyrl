from __future__ import absolute_import, division, print_function, unicode_literals

from level import Level
from collections import defaultdict
from level_template import LevelTemplate, LevelLocation
from game_data.player import Player


class LevelNotFound(Exception): pass


def _zero_factory():
    return 0


class World(object):

    def __init__(self):
        self.levels = {}
        self.level_templates = {}
        self.dungeon_lengths = defaultdict(_zero_factory)
        self.player = Player()

    def add_level_template(self, dungeon_key, level_template=None):
        self.dungeon_lengths[dungeon_key] += 1
        level_i = self.dungeon_lengths[dungeon_key]

        if level_template is None:
            level_template = LevelTemplate(level_i, tiles=None, static_creatures=(),
                                           creature_spawning=True)

        infos = level_template.passage_destination_infos
        infos[LevelLocation.Passage_Up] = (dungeon_key, level_i - 1), LevelLocation.Passage_Down
        infos[LevelLocation.Passage_Down] = (dungeon_key, level_i + 1), LevelLocation.Passage_Up

        self.level_templates[dungeon_key, level_i] = level_template

    def get_level(self, world_loc, visible_change_callback):
        if world_loc not in self.levels:
            if world_loc not in self.level_templates:
                raise LevelNotFound("Nonexistant level key: {}".format(world_loc))
            level_template = self.level_templates[world_loc]
            level_template.finalize()
            level = Level(world_loc, level_template, visible_change_callback)
            self.levels[world_loc] = level

        return self.levels[world_loc]
