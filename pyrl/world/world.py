from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from pyrl.types.level_key import LevelKey
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.creature.player import Player
from pyrl.types.world_point import WorldPoint
from pyrl.world.level import Level
from pyrl.world.level_gen_params import LevelGenParams

@dataclass
class World:
    player: Player
    time: int                                       = field(init=False, default=0)
    levels: dict[LevelKey, Level]                   = field(init=False, default_factory=dict)
    level_params: dict[LevelKey, LevelGenParams]    = field(init=False, default_factory=dict)
    level_connections: dict[WorldPoint, WorldPoint] = field(init=False, default_factory=dict)
    dungeon_lengths: Counter[str]                   = field(init=False, default_factory=Counter)

    def add_level(self, dungeon_key: str, level_params: LevelGenParams | None = None) -> None:
        self.dungeon_lengths[dungeon_key] += 1
        level_i = self.dungeon_lengths[dungeon_key]
        curr_level_key = LevelKey(dungeon_key, level_i)
        prev_level_key = LevelKey(dungeon_key, level_i - 1)

        if level_params is None:
            level_params = LevelGenParams(level_i)

        self.level_params[curr_level_key] = level_params
        if level_i != 1:
            previous_level_params = self.level_params[prev_level_key]

            passage_down = DefaultLocation.Passage_Down
            passage_up = DefaultLocation.Passage_Up
            if previous_level_params.will_have_location(passage_down) and level_params.will_have_location(passage_up):
                prev_level_point = WorldPoint(prev_level_key, passage_down)
                cur_level_point = WorldPoint(curr_level_key, passage_up)
                self.set_two_way_connection(prev_level_point, cur_level_point)

    def get_level(self, level_key: LevelKey) -> Level:
        if level_key not in self.levels:
            self.generate_level(level_key)
        return self.levels[level_key]

    def generate_level(self, level_key: LevelKey) -> None:
        if level_key not in self.level_params:
            raise KeyError(f"Nonexistant level key: {level_key}")

        self.levels[level_key] = self.level_params.pop(level_key).create_level(level_key)

    def has_destination(self, world_point: WorldPoint) -> bool:
        return world_point in self.level_connections

    def get_destination(self, world_point: WorldPoint) -> WorldPoint:
        return self.level_connections[world_point]

    def set_two_way_connection(self, point_a: WorldPoint, point_b: WorldPoint, do_assert: bool = True) -> None:
        if do_assert:
            level_params_a = self.level_params[point_a.level_key]
            level_params_b = self.level_params[point_b.level_key]
            assert level_params_a.will_have_location(point_a.level_location), \
                f"{level_params_a} doesn't have location {point_a.level_location}."
            assert level_params_b.will_have_location(point_b.level_location), \
                f"{level_params_b} doesn't have location {point_b.level_location}."

        self.set_connection(point_a, point_b)
        self.set_connection(point_b, point_a)

    def set_connection(self, point_a: WorldPoint, point_b: WorldPoint) -> None:
        self.level_connections[point_a] = point_b
