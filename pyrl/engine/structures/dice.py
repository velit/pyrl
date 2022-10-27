from __future__ import annotations

from dataclasses import dataclass
from random import randint

@dataclass(frozen=True)
class Dice:
    dices: int
    faces: int
    addition: int

    def roll(self) -> int:
        return sum(randint(0, self.faces) for _ in range(self.dices)) + self.addition

    def __str__(self) -> str:
        min_roll = self.addition
        max_roll = self.dices * self.faces + self.addition
        min_roll_str = f"({min_roll})" if min_roll < 0 else str(min_roll)
        max_roll_str = f"({max_roll})" if max_roll < 0 else str(max_roll)
        return f"{min_roll_str}-{max_roll_str}"
