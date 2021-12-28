from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING

from pyrl.types.char import Glyph
from pyrl.types.coord import Coord
from pyrl.structures.dice import Dice
from pyrl.creature.actions import Action
from pyrl.algorithms.coord_algorithms import resize_range

if TYPE_CHECKING:
    from pyrl.world.level import Level

@dataclass(eq=False, slots=True)
class Creature:
    name:                str
    char:              Glyph
    danger_level:        int = 0
    spawn_weight_class:  int = 1

    hp:                  int = field(init=False, repr=True)

    coord:             Coord = field(init=False, repr=False)
    level:             Level = field(init=False, repr=False)
    base_strength:       int = field(init=False, repr=False, default=10)
    base_dexterity:      int = field(init=False, repr=False, default=10)
    base_endurance:      int = field(init=False, repr=False, default=10)
    base_intelligence:   int = field(init=False, repr=False, default=10)
    base_perception:     int = field(init=False, repr=False, default=10)

    def __post_init__(self) -> None:
        self.hp = self.max_hp

    @property
    def damage_dice(self) -> Dice:
        base_attack_dices = self.strength // 20 + 1
        base_attack_faces = self.strength // 3 + self.dexterity // 6
        return Dice(base_attack_dices, base_attack_faces, self.damage)

    def receive_damage(self, amount: int) -> None:
        if amount > 0:
            self.hp -= amount

    def is_dead(self) -> bool:
        return self.hp <= 0

    def action_cost(self, action: Action, multiplier: float = 1.0) -> int:
        return round(action.base_cost * multiplier * self.speed_multiplier)

    def __repr__(self) -> str:
        return f"Creature(name={self.name})"

    def copy(self) -> Creature:
        return deepcopy(self)

    def spawn_weight(self, external_danger_level: int) -> int:
        return round(1000 * self.danger_level_spawn_mult(external_danger_level) * self.spawn_weight_class)

    def danger_level_spawn_mult(self, external_danger_level: int) -> Decimal:
        diff = Decimal(external_danger_level - self.danger_level)

        speciation_range = range(-5, 1)
        extant_range = range(1, 10)
        extinction_range = range(10, 21)
        if diff in speciation_range:
            # 0 0.008 0.064 0.216 0.512 1
            diff_weight = pow(resize_range(diff, speciation_range), 3)
        elif diff in extant_range:
            diff_weight = Decimal(1)
        elif diff in extinction_range:
            # 1, 0.999, 0.992, 0.973, 0.936, 0.875, 0.784, 0.657, 0.488, 0.271, 0
            diff_weight = Decimal(1 - pow(resize_range(diff, extinction_range), 3))
        else:
            diff_weight = Decimal(0)
        return diff_weight

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
    def speed(self) -> int:
        return 93 + self.dexterity // 2 + self.strength // 5

    @property
    def speed_multiplier(self) -> float:
        return 100 / self.speed

