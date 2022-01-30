from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING, Protocol

from pyrl.structures.dice import Dice

if TYPE_CHECKING:
    from pyrl.creature.creature import Creature

class Attackeable(Protocol):
    name: str

    @property
    def defense(self) -> int:
        raise NotImplementedError

    @property
    def armor(self) -> int:
        raise NotImplementedError

def calc_melee_attack(creature: Creature, target: Attackeable) -> tuple[bool, int]:
    """Get the result of a melee attack. Returns success and damage."""
    return _calc_melee_attack(creature.damage_dice, creature.accuracy, target.defense, target.armor)

def _calc_melee_attack(damage_dice: Dice, accuracy: int, defense: int, armor: int) -> tuple[bool, int]:
    roll = randint(1, 100) + accuracy - defense
    if roll > 25:
        return True, max(damage_dice.roll() - armor, 0)
    else:
        return False, 0
