from dataclasses import dataclass
from enum import Enum

from pyrl.dice import Dice


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

@dataclass(kw_only=True, slots=True)
class Stats:
    strength:            int = 0
    dexterity:           int = 0
    intelligence:        int = 0
    endurance:           int = 0
    perception:          int = 0
    sight:               int = 0
    max_hp:              int = 0
    armor:               int = 0
    accuracy:            int = 0
    defense:             int = 0
    speed:               int = 0
    damage:              int = 0
    weapon_dice: Dice | None = None
