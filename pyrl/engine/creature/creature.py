from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from pyrl.engine.actions.action import Action
from pyrl.engine.behaviour.coordinates import vector_within_distance
from pyrl.engine.creature.stats import Stat
from pyrl.engine.structures.dice import Dice
from pyrl.engine.types.directions import Coord
from pyrl.engine.types.glyphs import Glyph

if TYPE_CHECKING:
    from pyrl.engine.world.level import Level

@runtime_checkable
@dataclass(eq=False)
class Creature(Protocol):
    ticks:             int   = field(init=False, repr=True, default=0)
    hp:                int   = field(init=False, repr=False, default=0)
    coord:             Coord = field(init=False, repr=False)
    level:             Level = field(init=False, repr=False)

    def __post_init__(self) -> None:
        return

    def __getitem__(self, stat: Stat) -> int:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def glyph(self) -> Glyph:
        raise NotImplementedError

    @property
    def creature_level(self) -> int:
        return 0

    @property
    def damage_dice(self) -> Dice:
        base_attack_dices = self[Stat.STR] // 3 + self[Stat.DEX] // 6
        base_attack_faces = self[Stat.STR] // 20 + 1
        return Dice(base_attack_dices, base_attack_faces, self[Stat.DMG])

    @property
    def speed_multiplier(self) -> float:
        return 100 / self[Stat.SPEED]

    def advance_time(self, new_time: int) -> None:
        """Accrue all the passive changes that happen to this creature when time advances."""
        tick_delta = new_time - self.ticks
        if tick_delta > 0:
            self.apply_turn_effects(tick_delta)
        self.ticks = new_time

    def apply_turn_effects(self, tick_delta: int) -> None:
        self._apply_regen(tick_delta)

    def _apply_regen(self, time_delta: int) -> None:
        ticks_per_hp = 10000 / self[Stat.REGEN]
        previous_time = self.ticks % ticks_per_hp
        self.hp += int((previous_time + time_delta) / ticks_per_hp)
        self.hp = min(self.hp, self[Stat.MAX_HP])

    def receive_damage(self, amount: int) -> None:
        if amount > 0:
            self.hp -= amount

    def gain_kill_xp(self, target: Creature) -> tuple[int, Sequence[int]]:
        return 0, []

    def is_dead(self) -> bool:
        return self.hp <= 0

    def action_cost(self, action: Action, multiplier: float = 1.0) -> int:
        return round(action.base_cost * multiplier * self.speed_multiplier)

    def can_see(self, target_coord: Coord) -> bool:
        return (vector_within_distance(self.coord, target_coord, self[Stat.SIGHT]) and
                self.level.check_los(self.coord, target_coord))