from collections import Counter, namedtuple

from pyrl.enums.level_location import LevelLocation
from pyrl.world.level import Level

class LevelNotFound(Exception):
    pass

LevelKey = namedtuple("LevelKey", ("dungeon", "index"))
WorldPoint = namedtuple("WorldPoint", ("level_key", "level_location"))

class World:

    def __init__(self, player):
        self.levels = {}
        self.level_connections = {}
        self.dungeon_lengths = Counter()
        self.player = player
        self.start_level_key = None

    def add_level(self, dungeon_key, level=None):
        self.dungeon_lengths[dungeon_key] += 1
        level_i = self.dungeon_lengths[dungeon_key]
        curr_level_key = LevelKey(dungeon_key, level_i)
        prev_level_key = LevelKey(dungeon_key, level_i - 1)

        if level is None:
            level = Level(level_i)

        self.levels[curr_level_key] = level
        if level_i != 1:
            previous_level = self.levels[prev_level_key]

            passage_down = LevelLocation.Passage_Down
            passage_up = LevelLocation.Passage_Up
            if previous_level.will_have_location(passage_down) and level.will_have_location(passage_up):
                prev_level_point = WorldPoint(prev_level_key, passage_down)
                cur_level_point = WorldPoint(curr_level_key, passage_up)
                self.set_two_way_connection(prev_level_point, cur_level_point)

    def get_level(self, level_key):
        if level_key not in self.levels:
            raise LevelNotFound("Nonexistant level key: {}".format(level_key))

        level = self.levels[level_key]
        if not level.is_finalized:
            level.finalize(level_key)
        return level

    def has_destination(self, world_point):
        return world_point in self.level_connections

    def get_destination(self, world_point):
        return self.level_connections[world_point]

    def set_two_way_connection(self, world_point_a, world_point_b, do_assert=True):

        if do_assert:
            level_a = self.levels[world_point_a.level_key]
            level_b = self.levels[world_point_b.level_key]
            assert level_a.will_have_location(world_point_a.level_location), \
                "{} doesn't have location {}.".format(level_a, world_point_a.level_location)
            assert level_b.will_have_location(world_point_b.level_location), \
                "{} doesn't have location {}.".format(level_b, world_point_b.level_location)

        self.set_connection(world_point_a, world_point_b)
        self.set_connection(world_point_b, world_point_a)

    def set_connection(self, world_point_a, world_point_b):
        self.level_connections[world_point_a] = world_point_b
