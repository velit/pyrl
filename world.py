from __future__ import absolute_import, division, print_function, unicode_literals

from collections import defaultdict

from level import Level, LevelLocation
from level_template import LevelTemplate


class LevelNotFound(Exception): pass


def _zero_factory():
    return 0


class World(object):

    def __init__(self, player):
        self.levels = {}
        self.level_templates = {}
        self.dungeon_lengths = defaultdict(_zero_factory)
        self.player = player
        self.start_level = None

    def add_level_template(self, dungeon_key, level_template=None):
        self.dungeon_lengths[dungeon_key] += 1
        level_i = self.dungeon_lengths[dungeon_key]
        wloc = dungeon_key, level_i
        prev_wloc = dungeon_key, level_i - 1

        if level_template is None:
            level_template = LevelTemplate(level_i)

        if level_i != 1:
            previous_template = self.level_templates[prev_wloc]

            passage_down = LevelLocation.Passage_Down
            passage_up = LevelLocation.Passage_Up
            if (previous_template.will_have_location(passage_down) and level_template.will_have_location(passage_up)):
                previous_template.add_exit_info(passage_down, (wloc, passage_up))
                level_template.add_exit_info(passage_up, (prev_wloc, passage_down))

        self.level_templates[wloc] = level_template

    def get_level(self, world_loc, visible_change_callback):
        if world_loc not in self.levels:
            if world_loc not in self.level_templates:
                raise LevelNotFound("Nonexistant level key: {}".format(world_loc))
            level = Level(world_loc, self.level_templates[world_loc].finalize())
            level.visible_change.subscribe(visible_change_callback)
            self.levels[world_loc] = level

        return self.levels[world_loc]

    def add_two_way_connection(self, wlocA, locA, wlocB, locB, do_assert=True):
        A = self.level_templates[wlocA]
        B = self.level_templates[wlocB]

        if do_assert:
            assert A.will_have_location(locA), \
                "{} doesn't have location {}.".format(A, locA)
            assert B.will_have_location(locB), \
                "{} doesn't have location {}.".format(B, locB)

        self.add_one_way_connection(A, locA, (wlocB, locB))
        self.add_one_way_connection(B, locB, (wlocA, locA))

    def add_one_way_connection(self, level_template, source_location, exit_info):
        level_template.add_exit_info(source_location, exit_info)
