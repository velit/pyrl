from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass, field
from decimal import Decimal
from math import sqrt
from typing import Final

from pyrl.engine.behaviour.coordinates import resize_range
from pyrl.engine.creature.creature import Creature

@dataclass(eq=False)
class Learner(Creature):
    """Creatures with this mixin class learn new things and gain levels."""

    experience:     int        = field(init=False, default=0)
    levelups:       deque[int] = field(init=False, repr=False, default_factory=lambda: deque(range(2, 101)))

    kill_xp_unit:   Final[int] = field(init=False, repr=False, default=50)
    level_xp_unit:  Final[int] = field(init=False, repr=False, default=1000)

    @property
    def experience_level(self) -> int:
        return self.calc_experience_level(self.experience, self.level_xp_unit)

    def gain_kill_xp(self, target: Creature) -> tuple[int, Sequence[int]]:
        creature_xp = self.kill_xp_unit * target.creature_level
        levels_above = self.creature_level - target.creature_level

        still_xp = range(7) # Actually being 6 above won't give exp, 5 is max
        if levels_above in still_xp:
            xp_multi = Decimal(1 - pow(resize_range(Decimal(levels_above), still_xp), 3))
        elif levels_above < 0:
            xp_multi = 1 + Decimal(0.02) * abs(levels_above)
        else:
            xp_multi = Decimal(0)
        kill_xp = round(creature_xp * xp_multi)
        levelups = self.gain_xp(kill_xp)
        return kill_xp, levelups

    def gain_xp(self, amount: int) -> Sequence[int]:
        self.experience += amount
        levels = []
        while self.experience_level >= self.levelups[0]:
            level = self.levelups.popleft()
            levels.append(level)
            self.level_up(level)
        return levels

    def level_up(self, level: int) -> None:
        self.base_strength     += 2 * level
        self.base_dexterity    += 2 * level
        self.base_endurance    += 2 * level
        self.base_intelligence += 2 * level
        self.base_perception   += 2 * level

    @classmethod
    def calc_experience_level(cls, experience: int, base_level_xp: int) -> int:
        level_units = experience / base_level_xp
        inner_sqrt = 2 * level_units - 1
        if inner_sqrt < 0:
            return 1
        else:
            return int(sqrt(inner_sqrt) + 1) + 1

    @classmethod
    def calc_experience_limit(cls, level: int, level_unit_xp: int) -> int:
        """Return the xp limit for the given level."""
        level_units = level ** 2 / 2 - level + 1
        return int(level_units * level_unit_xp)
