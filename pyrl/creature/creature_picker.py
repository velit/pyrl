from __future__ import annotations

import random
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from pyrl.creature.creature import Creature
from pyrl.functions.coord_algorithms import resize_range

@dataclass(init=False, eq=False)
class CreaturePicker:
    total_weight: int
    weighted_creatures: list[tuple[int, Creature]]

    def __init__(self, creatures: Iterable[Creature] = (), danger_level: int = 0):
        self.set_creatures(creatures, danger_level)

    def set_creatures(self, creatures: Iterable[Creature], danger_level: int) -> None:
        self.weighted_creatures = []
        accumulator = 0
        for creature in creatures:
            weight = self.picking_weight(creature, danger_level)
            if weight == 0:
                continue
            accumulator += weight
            self.weighted_creatures.append((accumulator, creature))
        self.total_weight = accumulator

    def picking_weight(self, creature: Creature, area_level: int) -> int:
        return round(1000 * self.speciation_mult(area_level, creature.creature_level) * creature.spawn_class)

    def speciation_mult(self, creature_level: int, area_level: int) -> Decimal:
        """Applies a multiplier based on the difference of creature level to area level."""
        diff = area_level - creature_level
        speciation_range = range(-5, 1) # [-5, 0]
        extant_range     = range(1, 10)
        extinction_range = range(10, 21)
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

    def random_creature(self) -> Creature:
        if not self.weighted_creatures:
            raise IndexError("Trying to spawn a random creature with no creatures defined")
        index = random.randrange(self.total_weight)
        return next(creature for (slot, creature) in self.weighted_creatures if index < slot).copy()
