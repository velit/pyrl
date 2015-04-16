from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum


class Stat(Enum):
    strength       = "Str"
    dexterity      = "Dex"
    intelligence   = "Int"
    endurance      = "End"
    perception     = "Per"
    sight          = "Sight"
    max_hp         = "HP"
    armor          = "Armor"
    attack_rating  = "AR"
    defense_rating = "DR"
    speed          = "Speed"
    unarmed_dices  = "Unarmed dices"
    unarmed_sides  = "Unarmed sides"
    damage         = "Dmg"


def ensure_stats(obj):
    for stat in Stat:
        if not hasattr(obj, stat.name):
            error_msg = "Attribute {} must be found in {}".format(stat.name, obj)
            raise AssertionError(error_msg)
    return obj
