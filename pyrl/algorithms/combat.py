from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING, Protocol

from pyrl.structures.dice import Dice

if TYPE_CHECKING:
    from pyrl.creature.creature import Creature

class Attackeable(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def defense(self) -> int:
        raise NotImplementedError

    @property
    def armor(self) -> int:
        raise NotImplementedError

def get_melee_attack_cr(creature: Creature, target: Attackeable) -> tuple[bool, int]:
    return get_melee_attack(creature.damage_dice, creature.accuracy, target.defense, target.armor)

def get_melee_attack(damage_dice: Dice, accuracy: int, defense: int, armor: int) -> tuple[bool, int]:
    roll = randint(1, 100) + accuracy - defense
    if roll > 25:
        return True, max(damage_dice.roll() - armor, 0)
    else:
        return False, 0

def get_combat_message(attack_succeeds: bool, damage: int, dies: bool, player_attacker: bool,
                       player_target: bool, attacker_name: str, defender_name: str) -> str:

    if player_attacker:
        attacker = "You"
        third_person_singular = False
    else:
        attacker = f"The {attacker_name}"
        third_person_singular = True

    if player_attacker and player_target:
        target = "yourself"
        indirect_target = "yourself"
    elif player_target:
        target = "you"
        indirect_target = "you"
    else:
        target = f"the {defender_name}"
        indirect_target = "it"

    if third_person_singular:
        s = "s"
        es = "es"
    else:
        s = ""
        es = ""

    message = ""
    if damage:
        message += f"{attacker} hit{s} {target} for {damage} damage"
        if dies:
            message += f" and kill{s} {indirect_target}."
        else:
            message += "."
    elif attack_succeeds:
        message += f"{attacker} fail{s} to hurt {target}."
    else:
        message += f"{attacker} miss{es} {target}."
    return message
