from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from pyrl.engine.creature.enums.stats import StatsProvider, Stats, Stat


class Skill(Enum):
    HEALING = "Healing", "Long term healing."
    SCROUNGING = "Scrounging", "Ability to find vital supplies."

    def __init__(self, skill_name: str, skill_description: str) -> None:
        self.skill_name = skill_name
        self.skill_description = skill_description

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self.name}>"


@dataclass(eq=False)
class Skills(StatsProvider):

    skills: Counter[Skill]

    def stats_sources(self) -> Iterable[Stats]:
        stats = Stats()
        if Skill.HEALING in self.skills:
            stats[Stat.REGEN] += self.skills[Skill.HEALING] // 20
        yield stats
