from __future__ import annotations

from collections import Counter

from pyrl.types.level_key import LevelKey
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.creature.player import Player
from pyrl.types.world_point import WorldPoint
from pyrl.world.level import Level

class World:

    def __init__(self, player: Player) -> None:
        self.levels: dict[LevelKey, Level] = {}
        self.level_connections: dict[WorldPoint, WorldPoint] = {}
        self.dungeon_lengths: Counter[str] = Counter()
        self.player: Player = player
        self.start_level_key = None

    def add_level(self, dungeon_key: str, level: Level | None = None) -> None:
        self.dungeon_lengths[dungeon_key] += 1
        level_i = self.dungeon_lengths[dungeon_key]
        curr_level_key = LevelKey(dungeon_key, level_i)
        prev_level_key = LevelKey(dungeon_key, level_i - 1)

        if level is None:
            level = Level(level_i)

        self.levels[curr_level_key] = level
        if level_i != 1:
            previous_level = self.levels[prev_level_key]

            passage_down = DefaultLocation.Passage_Down
            passage_up = DefaultLocation.Passage_Up
            if previous_level.will_have_location(passage_down) and level.will_have_location(passage_up):
                prev_level_point = WorldPoint(prev_level_key, passage_down)
                cur_level_point = WorldPoint(curr_level_key, passage_up)
                self.set_two_way_connection(prev_level_point, cur_level_point)

    def get_level(self, level_key: LevelKey) -> Level:
        if level_key not in self.levels:
            raise KeyError(f"Nonexistant level key: {level_key}")

        level = self.levels[level_key]
        if not level.is_finalized:
            level.finalize(level_key)
        return level

    def has_destination(self, world_point: WorldPoint) -> bool:
        return world_point in self.level_connections

    def get_destination(self, world_point: WorldPoint) -> WorldPoint:
        return self.level_connections[world_point]

    def set_two_way_connection(self, point_a: WorldPoint, point_b: WorldPoint, do_assert: bool = True) -> None:

        if do_assert:
            level_a = self.levels[point_a.level_key]
            level_b = self.levels[point_b.level_key]
            assert level_a.will_have_location(point_a.level_location), \
                f"{level_a} doesn't have location {point_a.level_location}."
            assert level_b.will_have_location(point_b.level_location), \
                f"{level_b} doesn't have location {point_b.level_location}."

        self.set_connection(point_a, point_b)
        self.set_connection(point_b, point_a)

    def set_connection(self, point_a: WorldPoint, point_b: WorldPoint) -> None:
        self.level_connections[point_a] = point_b
