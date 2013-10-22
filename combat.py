from random import randint
from dice import dice_roll


def get_melee_attack(ar, damage_info, dr, pv):
    roll = randint(1, 100) + ar - dr
    if roll > 25:
        return (True, max(dice_roll(*damage_info) - pv, 0))
    else:
        return (False, 0)


def get_combat_message(attack_succeeds, damage, dies, personity, attacker_name=None, defender_name=None):
    subject_is_player, object_is_player = personity
    message = ""
    if subject_is_player:
        A = "You"
        s = ""
        s2 = ""
    else:
        A = "The {}".format(attacker_name)
        s = "s"
        s2 = "es"
    if object_is_player:
        t = "you"
        i = "you"
    else:
        t = "the {}".format(defender_name)
        i = "it"
    if subject_is_player and object_is_player:
        t = "yourself"
        i = "yourself"
        mv = "trying to hit "
    else:
        mv = ""

    if damage:
        message += "{} hit{} {} for {} damage".format(A, s, t, damage)
        message += " and kill{} {}.".format(s, i) if dies else "."
    elif attack_succeeds:
        message += "{} fail{} to hurt {}.".format(A, s, t)
    else:
        message += "{} miss{} {}{}.".format(A, s2, mv, t)
    return message
