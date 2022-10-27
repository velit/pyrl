from __future__ import annotations

from collections.abc import Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pyrl.engine.actions.action import Action
from pyrl.engine.behaviour.combat import Attackeable
from pyrl.engine.behaviour.coordinates import vector_within_distance
from pyrl.engine.structures.dice import Dice
from pyrl.engine.types.directions import Coord
from pyrl.engine.types.glyphs import Glyph

if TYPE_CHECKING:
    from pyrl.engine.world.level import Level

@dataclass(eq=False)
class Creature(Attackeable):
    name:              str
    glyph:             Glyph
    creature_level:    int = 0
    spawn_class:       int = field(repr=False, default=1)

    base_strength:     int = field(init=False, repr=False)
    base_dexterity:    int = field(init=False, repr=False)
    base_endurance:    int = field(init=False, repr=False)
    base_intelligence: int = field(init=False, repr=False)
    base_perception:   int = field(init=False, repr=False)

    turns:             int = field(init=False, repr=False, default=0)
    time:              int = field(init=False, repr=True, default=0)

    hp:                int = field(init=False, repr=True)
    coord:           Coord = field(init=False, repr=True)
    level:           Level = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.base_strength     = 10 + self.creature_level
        self.base_dexterity    = 10 + self.creature_level
        self.base_endurance    = 10 + self.creature_level
        self.base_intelligence = 10 + self.creature_level
        self.base_perception   = 10 + self.creature_level

        self.hp = self.max_hp

    def advance_time(self, new_time: int) -> None:
        """Accrue all the passive changes that happen to this creature when time advances."""
        time_delta = new_time - self.time
        if time_delta > 0:
            self.apply_regen(time_delta)
            self.turns += 1
        self.time = new_time

    def apply_regen(self, time_delta: int) -> None:
        ticks_per_hp = 4000 / self.regen
        previous_time = self.time % ticks_per_hp
        self.hp += int((previous_time + time_delta) / ticks_per_hp)
        self.hp = min(self.hp, self.max_hp)

    @property
    def damage_dice(self) -> Dice:
        base_attack_dices = self.strength // 3 + self.dexterity // 6
        base_attack_faces = self.strength // 20 + 1
        return Dice(base_attack_dices, base_attack_faces, self.damage)

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
        return (vector_within_distance(self.coord, target_coord, self.sight) and
                self.level.check_los(self.coord, target_coord))

    def __repr__(self) -> str:
        return f"Creature(name={self.name})"

    def copy(self) -> Creature:
        return deepcopy(self)

    @property
    def strength(self) -> int:
        return self.base_strength

    @property
    def dexterity(self) -> int:
        return self.base_dexterity

    @property
    def intelligence(self) -> int:
        return self.base_intelligence

    @property
    def endurance(self) -> int:
        return self.base_endurance

    @property
    def perception(self) -> int:
        return self.base_perception

    @property
    def accuracy(self) -> int:
        return self.dexterity + self.perception // 2

    @property
    def armor(self) -> int:
        return self.endurance // 10

    @property
    def damage(self) -> int:
        return self.strength // 5 + self.dexterity // 10

    @property
    def defense(self) -> int:
        return self.dexterity + self.intelligence // 2

    @property
    def max_hp(self) -> int:
        return self.endurance + self.strength // 2

    @property
    def sight(self) -> int:
        return min(self.perception // 2, int((self.perception * 5) ** 0.5))

    @property
    def regen(self) -> float:
        """HP per 4000 time units."""
        return 0.5 + 1 * self.endurance / 20

    @property
    def speed(self) -> int:
        return 93 + self.dexterity // 2 + self.strength // 5

    @property
    def speed_multiplier(self) -> float:
        return 100 / self.speed
