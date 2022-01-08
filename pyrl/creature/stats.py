from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import Type

class Stat(Enum):
    strength       = "Str"
    dexterity      = "Dex"
    intelligence   = "Int"
    endurance      = "End"
    perception     = "Per"
    accuracy       = "Acc"
    armor          = "Armor"
    damage         = "Dmg"
    defense        = "Def"
    max_hp         = "HP"
    sight          = "Sight"
    speed          = "Speed"

@dataclass(kw_only=True)
class Stats:
    strength:            int = 0
    dexterity:           int = 0
    intelligence:        int = 0
    endurance:           int = 0
    perception:          int = 0
    accuracy:            int = 0
    armor:               int = 0
    damage:              int = 0
    defense:             int = 0
    max_hp:              int = 0
    sight:               int = 0
    speed:               int = 0

    @classmethod
    def combine(cls: Type[Stats], *stats_instances: Stats) -> Stats:
        combined = cls()
        for stats in stats_instances:
            for key, value in dataclasses.asdict(stats).items():
                setattr(combined, key, getattr(combined, key) + value)
        return combined
