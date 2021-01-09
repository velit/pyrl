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
    accuracy       = "Acc"
    defense        = "Def"
    speed          = "Speed"
    damage         = "Dmg"

class ComplexStat(Enum):
    weapon_dice = "Damage"

def ensure_stats(obj):
    for stat in Stat:
        assert hasattr(obj, stat.name), f"Attribute {stat.name} must be found in {obj}"
    return obj
