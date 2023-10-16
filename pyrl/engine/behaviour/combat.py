from __future__ import annotations

from random import randint

from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.enums.stats import Stat
from pyrl.engine.structures.dice import Dice
from pyrl.engine.world.tile import Tile


def calc_melee_attack(creature: Creature, target: Creature | Tile) -> tuple[bool, int]:
    """Get the result of a melee attack. Returns success and damage."""
    match target:
        case Creature() as target_creature:
            return _calc_melee_attack(creature.damage_dice, creature[Stat.ACC],
                                      target_creature[Stat.DEF], target_creature[Stat.ARMOR])
        case Tile() as tile:
            return _calc_melee_attack(creature.damage_dice, creature[Stat.ACC],
                                      1, 100 if tile.is_passable else 40)

def _calc_melee_attack(damage_dice: Dice, accuracy: int, defense: int, armor: int) -> tuple[bool, int]:
    roll = randint(1, 100) + accuracy - defense
    if roll > 25:
        return True, max(damage_dice.roll() - armor, 0)
    else:
        return False, 0
