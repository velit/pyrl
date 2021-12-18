from dataclasses import dataclass
from random import randint

@dataclass(frozen=True, slots=True)
class Dice:
    dices: int
    faces: int
    addition: int

    def roll(self):
        return sum(randint(0, self.faces) for _ in range(self.dices)) + self.addition

    def __str__(self):
        min_roll = self.addition
        max_roll = self.dices * self.faces + self.addition
        if min_roll < 0:
            min_roll = f"({min_roll})"
        if max_roll < 0:
            max_roll = f"({max_roll}"
        return f"{min_roll}-{max_roll}"
