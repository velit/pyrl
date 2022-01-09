from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pyrl.creature.action import Action
from pyrl.structures.dice import Dice
from pyrl.types.char import Glyph
from pyrl.types.coord import Coord

if TYPE_CHECKING:
    from pyrl.world.level import Level

@dataclass(eq=False)
class Creature:
    name:              str
    char:            Glyph
    creature_level:    int = 0
    spawn_class:       int = 1

    base_strength:     int = field(init=False, repr=False, default=10)
    base_dexterity:    int = field(init=False, repr=False, default=10)
    base_endurance:    int = field(init=False, repr=False, default=10)
    base_intelligence: int = field(init=False, repr=False, default=10)
    base_perception:   int = field(init=False, repr=False, default=10)

    hp:                int = field(init=False, repr=True)
    coord:           Coord = field(init=False, repr=True)
    level:           Level = field(init=False, repr=False)

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

    def kill(self, target: Creature) -> None:
        pass

    def is_dead(self) -> bool:
        return self.hp <= 0

    def action_cost(self, action: Action, multiplier: float = 1.0) -> int:
        return round(action.base_cost * multiplier * self.speed_multiplier)

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
    def speed(self) -> int:
        return 93 + self.dexterity // 2 + self.strength // 5

    @property
    def speed_multiplier(self) -> float:
        return 100 / self.speed
