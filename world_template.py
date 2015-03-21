from __future__ import absolute_import, division, print_function, unicode_literals

from collections import defaultdict

import const.game as GAME
from level_template import LevelTemplate


class LevelNotFound(Exception):
    pass


def _zero_factory():
    return 0


class WorldTemplate(object):

    def __init__(self):
        self.level_templates = {}
        self.dungeon_lengths = defaultdict(_zero_factory)
        self.first_level_info = None

    def add_first_level_info(self, wloc, passage):
        self.first_level_info = wloc, passage

    def add_level(self, dungeon_key, level_template=None):
        self.dungeon_lengths[dungeon_key] += 1
        level_i = self.dungeon_lengths[dungeon_key]

        if level_template is None:
            level_template = LevelTemplate(level_i)

        infos = level_template.passage_destination_infos
        infos[GAME.PASSAGE_UP] = (dungeon_key, level_i - 1), GAME.PASSAGE_DOWN
        infos[GAME.PASSAGE_DOWN] = (dungeon_key, level_i + 1), GAME.PASSAGE_UP

        self.level_templates[dungeon_key, level_i] = level_template

    def get_level_template(self, world_loc):
        try:
            return self.level_templates[world_loc]
        except KeyError:
            raise LevelNotFound("Nonexistant level key: {}".format(world_loc))

    def pop_level_template(self, world_loc):
        try:
            level_template = self.level_templates[world_loc]
        except KeyError:
            raise LevelNotFound("Nonexistant level key: {}".format(world_loc))
        else:
            del self.level_templates[world_loc]
            return level_template
