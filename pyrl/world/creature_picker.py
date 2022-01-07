from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable

from pyrl.creature.creature import Creature

@dataclass(init=False, eq=False, slots=True)
class CreaturePicker:
    total_weight: int
    weighted_creatures: list[tuple[int, Creature]]

    def __init__(self, creatures: Iterable[Creature] = (), danger_level: int = 0):
        self.set_creatures(creatures, danger_level)

    def set_creatures(self, creatures: Iterable[Creature], danger_level: int) -> None:
        self.weighted_creatures = []
        accumulator = 0
        for creature in creatures:
            weight = creature.spawn_weight(danger_level)
            if weight == 0:
                continue
            accumulator += weight
            self.weighted_creatures.append((accumulator, creature))
        self.total_weight = accumulator

    def random_creature(self) -> Creature:
        if not self.weighted_creatures:
            raise IndexError("Trying to spawn a random creature with no creatures defined")
        index = random.randrange(self.total_weight)
        return next(creature for (slot, creature) in self.weighted_creatures if index < slot).copy()
