from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field
from decimal import Decimal
from math import sqrt
from typing import Final

from pyrl.creature.creature import Creature
from pyrl.functions.coord_algorithms import resize_range


@dataclass(eq=False)
class Learner(Creature):
    """Creatures with this mixin class learn new things and gain levels."""

    experience:     int        = field(init=False, default=0)
    levelups:       deque[int] = field(init=False, default_factory=lambda: deque(range(2, 101)))

    base_kill_xp:   Final[int] = field(init=False, default=50)
    base_level_xp:  Final[int] = field(init=False, default=1000)

    def kill(self, target: Creature) -> None:
        creature_xp = self.base_kill_xp * target.creature_level
        levels_above = self.creature_level - target.creature_level

        still_xp = range(7) # Actually being 6 above won't give exp, 5 is max
        if levels_above in still_xp:
            xp_multi = Decimal(1 - pow(resize_range(Decimal(levels_above), still_xp), 3))
        elif levels_above < 0:
            xp_multi = 1 + Decimal(0.02) * abs(levels_above)
        else:
            xp_multi = Decimal(0)
        kill_xp = round(creature_xp * xp_multi)
        self.gain_xp(kill_xp)

    def gain_xp(self, amount: int) -> None:
        self.experience += amount
        logging.debug(f"+{amount} xp")
        while self.experience_level >= self.levelups[0]:
            self.level_up(self.levelups.popleft())

    def xp_limit(self, level: int) -> int:
        """Return the xp limit for the given level."""
        return (level ** 2) / 2 - level + 1

    @property
    def experience_level(self) -> int:
        return int(sqrt(2 * self.experience / self.base_level_xp - 1) + 1)

    def level_up(self, level: int) -> None:
        logging.debug(f"You gain enough experience to attain level {level}!")
        self.base_strength += 2
        self.base_dexterity += 2
        self.base_endurance += 2
        self.base_intelligence += 2
        self.base_perception += 2
