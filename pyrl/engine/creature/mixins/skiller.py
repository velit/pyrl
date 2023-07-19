from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

from pyrl.engine.creature.mixins.stats_mutator import StatsMutator
from pyrl.engine.creature.skills import Skills

@dataclass(eq=False)
class Skiller(StatsMutator, ABC):
    """Creatures with this mixin class have skills that impact them."""

    skills: Skills

    def __post_init__(self) -> None:
        self.register_stat_source(self.skills)
        super().__post_init__()
