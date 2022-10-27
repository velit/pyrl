from __future__ import annotations

from pyrl.engine.behaviour.combat import Attackeable
from pyrl.engine.creature.creature import Creature

def experience_message(amount: int) -> str:
    return f"+[{amount}]"

def combat_message(attacker: Creature, target: Attackeable, player: Creature,
                   succeeds: bool, dies: bool, damage: int) -> str:
    player_attacker = attacker is player
    player_target = target is player
    if player_attacker:
        subject = "You"
        third_person_singular = False
    else:
        subject = f"The {attacker.name}"
        third_person_singular = True

    if player_attacker and player_target:
        object_ = "yourself"
        indirect_object = "yourself"
    elif player_target:
        object_ = "you"
        indirect_object = "you"
    else:
        object_ = f"the {target.name}"
        indirect_object = "it"

    if third_person_singular:
        s = "s"
        es = "es"
    else:
        s = ""
        es = ""

    message = ""
    if damage:
        message += f"{subject} hit{s} {object_} for {damage} damage"
        if dies:
            message += f" and kill{s} {indirect_object}."
        else:
            message += "."
    elif succeeds:
        message += f"{subject} fail{s} to hurt {object_}."
    else:
        message += f"{subject} miss{es} {object_}."
    return message
