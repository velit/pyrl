from random import randint

from pyrl.dice import dice_roll

def get_melee_attack_cr(creature, target):
    return get_melee_attack(creature.accuracy, creature.get_damage_info(),
                            target.defense, target.armor)

def get_melee_attack(accuracy, damage_info, defense, armor):
    roll = randint(1, 100) + accuracy - defense
    if roll > 25:
        return True, max(dice_roll(*damage_info) - armor, 0)
    else:
        return False, 0

def get_combat_message(attack_succeeds, damage, dies, player_attacker,
                       player_target, attacker_name, defender_name):

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
