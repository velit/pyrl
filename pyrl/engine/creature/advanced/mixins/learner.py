from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass, field
from decimal import Decimal
from math import sqrt
from typing import Final

from pyrl.engine.behaviour.coordinates import resize_range
from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.advanced.mixins.mutator import Mutator

@dataclass(eq=False)
class Learner(Mutator, ABC):
    """Creatures with this mixin class learn new things and gain levels."""

    experience:     int        = field(init=False, default=0)
    claimed_level:  int        = field(init=False, default=0)
    kill_xp_unit:   Final[int] = field(init=False, repr=False, default=50)
    level_xp_unit:  Final[int] = field(init=False, repr=False, default=1000)

    @property
    def creature_level(self) -> int:
        return self._calc_experience_level(self.experience, self.level_xp_unit)

    def gain_kill_xp(self, target: Creature) -> tuple[int, Sequence[int]]:
        """Returns earned xp normalized by level difference and potential levelups from the gained xp."""
        creature_xp = self.kill_xp_unit * target.creature_level
        levels_above = self.creature_level - target.creature_level

        still_xp = range(7)  # Actually being 6 above won't give exp, 5 is max
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
        if self.creature_level > self.claimed_level:
            while self.creature_level > self.claimed_level:
                self.claimed_level += 1
                levels.append(self.claimed_level)
                self.level_up(self.claimed_level)
            self.update_stats()

        return levels

    def level_up(self, level: int) -> None:
        # No effect yet
        pass

    @staticmethod
    def _calc_experience_level(experience: int, base_level_xp: int) -> int:
        level_units = experience / base_level_xp
        inner_sqrt = 2 * level_units - 1
        if inner_sqrt < 0:
            return 0
        else:
            return int(sqrt(inner_sqrt) + 1)

    @staticmethod
    def _calc_next_level_limit(level: int, level_unit_xp: int) -> int:
        """Return the next level xp limit for the given level."""
        next_level = level + 1
        level_units = next_level ** 2 / 2 - next_level + 1
        return int(level_units * level_unit_xp)
