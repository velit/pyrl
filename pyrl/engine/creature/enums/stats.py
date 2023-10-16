from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from enum import Enum
from typing import Protocol


class Stat(Enum):
    STR    = "Str",   "Strength",   "Description"
    DEX    = "Dex",   "Dexterity",  "Description"
    INT    = "Int",   "Intellect",  "Description"
    END    = "End",   "Endurance",  "Description"
    PER    = "Per",   "Perception", "Description"
    ACC    = "Acc",   "Accuracy",   "Description"
    ARMOR  = "Armor", "Armor",      "Description"
    DMG    = "Dmg",   "Damage",     "Description"
    DEF    = "Def",   "Defense",    "Description"
    MAX_HP = "HP",    "Max Health", "Description"
    REGEN  = "Regen", "Regen",      "Amount of HP you regen in ten standard turns"
    SIGHT  = "Sight", "Sight",      "Description"
    SPEED  = "Speed", "Speed",      "Description"

    def __init__(self, short_name: str, long_name: str, description: str) -> None:
        self.short_name = short_name
        self.long_name = long_name
        self.description = description

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self.name}>"

Stats = Counter[Stat]

class StatsProvider(Protocol):

    def stats_sources(self) -> Iterable[Stats]:
        raise NotImplementedError

def calculate_stats(creature_level: int, stats_providers: list[StatsProvider]) -> Stats:
    # Aggregate modifications
    new_stats: Stats = Counter()
    for stats_provider in stats_providers:
        for stats in stats_provider.stats_sources():
            new_stats.update(stats)

    # Base stats
    new_stats[Stat.STR]    += 10 + creature_level
    new_stats[Stat.DEX]    += 10 + creature_level
    new_stats[Stat.INT]    += 10 + creature_level
    new_stats[Stat.END]    += 10 + creature_level
    new_stats[Stat.PER]    += 10 + creature_level
    new_stats[Stat.SPEED]  += 93

    # Dependent modifications
    new_stats[Stat.MAX_HP] += new_stats[Stat.END]
    new_stats[Stat.MAX_HP] += new_stats[Stat.STR] // 2

    new_stats[Stat.ACC]    += new_stats[Stat.DEX]
    new_stats[Stat.ACC]    += new_stats[Stat.PER] // 2

    new_stats[Stat.DMG]    += new_stats[Stat.STR] // 5
    new_stats[Stat.DMG]    += new_stats[Stat.DEX] // 10

    new_stats[Stat.DEF]    += new_stats[Stat.DEX]
    new_stats[Stat.DEF]    += new_stats[Stat.INT] // 2

    new_stats[Stat.ARMOR]  += new_stats[Stat.END] // 10

    new_stats[Stat.SIGHT]  += min(new_stats[Stat.PER] // 2, int((new_stats[Stat.PER] * 5) ** 0.5))

    new_stats[Stat.SPEED]  += new_stats[Stat.DEX] // 2
    new_stats[Stat.SPEED]  += new_stats[Stat.STR] // 5

    new_stats[Stat.REGEN]  += new_stats[Stat.END] // 10

    # Clamps
    new_stats[Stat.SIGHT]  = max(0, new_stats[Stat.SIGHT])
    new_stats[Stat.REGEN]  = max(0, new_stats[Stat.REGEN])
    new_stats[Stat.SPEED]  = max(1, new_stats[Stat.SPEED])
    new_stats[Stat.MAX_HP] = max(1, new_stats[Stat.MAX_HP])

    return new_stats
