from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field

from pyrl.engine.creature.enums.traits import Trait
from pyrl.engine.creature.creature import Creature


@dataclass(eq=False)
class Traitful(Creature, ABC):
    """Creatures with this mixin class have traits that can impact them."""

    traits: set[Trait] = field(default_factory=set)
