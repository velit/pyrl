from abc import ABC
from collections import Counter
from dataclasses import dataclass, field

from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.enums.stats import Stats, StatsProvider, Stat, calculate_stats

@dataclass(eq=False)
class Mutator(Creature, ABC):
    """Creatures with this mixin class and the classes that inherit from this can modify the creature's stats."""

    stats:           Stats               = field(init=False, repr=False, default_factory=Counter[Stat])
    stats_providers: list[StatsProvider] = field(init=False, repr=False, default_factory=list)

    def __getitem__(self, stat: Stat) -> int:
        return self.stats[stat]

    def register_stat_source(self, stats_provider: StatsProvider) -> None:
        self.stats_providers.append(stats_provider)

    def update_stats(self) -> None:
        at_max_hp = self.hp == self[Stat.MAX_HP]
        self.stats = calculate_stats(self.creature_level, self.stats_providers if self.stats_providers else [])
        if at_max_hp:
            self.hp = self[Stat.MAX_HP]
        self.hp = min(self.hp, self[Stat.MAX_HP])

    def __post_init__(self) -> None:
        super().__post_init__()
        self.update_stats()
