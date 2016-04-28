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
        assert hasattr(obj, stat.name), "Attribute {} must be found in {}".format(stat.name, obj)
    return obj
