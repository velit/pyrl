from __future__ import annotations

import random
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Self

from pyrl.engine.behaviour.coordinates import resize_range
from pyrl.engine.creature.basic_creature import CreatureTemplate
from pyrl.engine.creature.creature import Creature

@dataclass(eq=False, frozen=True)
class CreaturePicker:
    weighted_creatures: list[tuple[int, CreatureTemplate]]
    total_weight: int

    @classmethod
    def using_speciation(cls, creature_templates: Iterable[CreatureTemplate], area_level: int) -> Self:
        weighted_creatures = []
        accumulator = 0
        for creature in creature_templates:
            weight = cls._picking_weight(area_level, creature)
            if weight == 0:
                continue
            accumulator += weight
            weighted_creatures.append((accumulator, creature))
        return cls(weighted_creatures, accumulator)

    def spawn_random_creature(self) -> Creature:
        if not self.weighted_creatures:
            raise IndexError("Trying to spawn a random creature with no creatures defined")
        index = random.randrange(self.total_weight)
        return next(creature_template.create() for (slot, creature_template) in self.weighted_creatures if index < slot)

    @classmethod
    def _picking_weight(cls, area_level: int, creature_template: CreatureTemplate) -> int:
        speciation_multiplier = cls._speciation_mult(area_level - creature_template.creature_level)
        return round(1000 * speciation_multiplier * creature_template.spawn_weight_class)

    @staticmethod
    def _speciation_mult(diff: int) -> Decimal:
        """Applies a multiplier based on the difference of usually creature level to area level."""
        speciation_range = range(-5, 1)   # [-5, 0]
        extant_range     = range(1, 10)   # [1, 9]
        extinction_range = range(10, 21)  # [10, 20]
        diff_weight: Decimal
        if diff in speciation_range:
            # 0 0.008 0.064 0.216 0.512 1
            diff_weight = pow(resize_range(Decimal(diff), speciation_range), 3)
        elif diff in extant_range:
            diff_weight = Decimal(1)
        elif diff in extinction_range:
            # 1, 0.999, 0.992, 0.973, 0.936, 0.875, 0.784, 0.657, 0.488, 0.271, 0
            diff_weight = Decimal(1 - pow(resize_range(Decimal(diff), extinction_range), 3))
        else:
            diff_weight = Decimal(0)
        return diff_weight
