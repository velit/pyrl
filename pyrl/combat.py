from random import randint

from pyrl.dice import dice_roll

def get_melee_attack_cr(creature, target):
    return get_melee_attack(creature.accuracy, creature.get_damage_info(),
                            target.defense, target.armor)

def get_melee_attack(accuracy, damage_info, defense, armor):
    roll = randint(1, 100) + accuracy - defense
    if roll > 25:
        return (True, max(dice_roll(*damage_info) - armor, 0))
    else:
        return (False, 0)

def get_combat_message(attack_succeeds, damage, dies, player_attacker,
                       player_target, attacker_name, defender_name):

    if player_attacker:
        attacker = "You"
        third_person_singular = False
    else:
        attacker = "The {}".format(attacker_name)
        third_person_singular = True

    if player_attacker and player_target:
        target = "yourself"
        indirect_target = "yourself"
    elif player_target:
        target = "you"
        indirect_target = "you"
    else:
        target = "the {}".format(defender_name)
        indirect_target = "it"

    if third_person_singular:
        s = "s"
        es = "es"
    else:
        s = ""
        es = ""

    message = ""
    if damage:
        message += "{} hit{} {} for {} damage".format(attacker, s, target, damage)
        if dies:
            message += " and kill{} {}.".format(s, indirect_target)
        else:
            message += "."
    elif attack_succeeds:
        message += "{} fail{} to hurt {}.".format(attacker, s, target)
    else:
        message += "{} miss{} {}.".format(attacker, es, target)
    return message
