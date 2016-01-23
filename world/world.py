from __future__ import absolute_import, division, print_function, unicode_literals

from collections import Counter

from world.level import Level, LevelLocation
from world.level_template import LevelTemplate


class LevelNotFound(Exception): pass


class World(object):

    def __init__(self, player):
        self.levels = {}
        self.level_templates = {}
        self.level_connections = {}
        self.dungeon_lengths = Counter()
        self.player = player
        self.start_level = None

    def add_level_template(self, dungeon_key, level_template=None):
        self.dungeon_lengths[dungeon_key] += 1
        level_i = self.dungeon_lengths[dungeon_key]
        curr_level_key = dungeon_key, level_i
        prev_level_key = dungeon_key, level_i - 1

        if level_template is None:
            level_template = LevelTemplate(level_i)

        if level_i != 1:
            previous_template = self.level_templates[prev_level_key]

            passage_down = LevelLocation.Passage_Down
            passage_up = LevelLocation.Passage_Up
            if (previous_template.will_have_location(passage_down) and level_template.will_have_location(passage_up)):
                self.set_connection((prev_level_key, passage_down), (curr_level_key, passage_up))
                self.set_connection((curr_level_key, passage_up), (prev_level_key, passage_down))

        self.level_templates[curr_level_key] = level_template

    def get_level(self, level_key, visible_change_callback):
        if level_key not in self.levels:
            if level_key not in self.level_templates:
                raise LevelNotFound("Nonexistant level key: {}".format(level_key))
            level = Level(level_key, self.level_templates[level_key].finalize())
            level.visible_change.subscribe(visible_change_callback)
            self.levels[level_key] = level

        return self.levels[level_key]

    def has_destination(self, world_point):
        return world_point in self.level_connections

    def get_destination(self, world_point):
        return self.level_connections[world_point]

    def add_two_way_connection(self, world_point_a, world_point_b, do_assert=True):

        if do_assert:
            level_key_a, level_loc_a = world_point_a
            level_key_b, level_loc_b = world_point_b
            level_a = self.level_templates[level_key_a]
            level_b = self.level_templates[level_key_b]
            assert level_a.will_have_location(level_loc_a), \
                "{} doesn't have location {}.".format(level_a, level_loc_a)
            assert level_b.will_have_location(level_loc_b), \
                "{} doesn't have location {}.".format(level_b, level_loc_b)

        self.set_connection(world_point_a, world_point_b)
        self.set_connection(world_point_b, world_point_a)

    def set_connection(self, world_point_a, world_point_b):
        self.level_connections[world_point_a] = world_point_b
