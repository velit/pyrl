from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

from pyrl.engine.creature.advanced.mixins.mutator import Mutator
from pyrl.engine.creature.advanced.skills import Skills

@dataclass(eq=False)
class Skiller(Mutator, ABC):
    """Creatures with this mixin class have skills that can impact them."""

    skills: Skills

    def __post_init__(self) -> None:
        self.register_stat_source(self.skills)
        super().__post_init__()
