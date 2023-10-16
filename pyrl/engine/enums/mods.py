from __future__ import annotations

from enum import Enum

inf = float("inf")

class Mod(Enum):
    NONEXISTENT    = "~0.00", "nonexistent", -inf
    N9             = "~0.13", "abysmal",     -9
    N8             = "~0.17", "dreadful",    -8
    N7             = "~0.21", "terrible",    -7
    N6             = "~0.26", "awful",       -6
    N5             = "~0.33", "bad",         -5
    N4             = "~0.41", "poor",        -4
    N3             = "~0.51", "inferior",    -3
    N2             = "~0.64", "deficient",   -2
    N1             = "~0.80", "mediocre",    -1
    P0             = "~1.00", "fair",         0
    P1             = "~1.20", "fine",         1
    P2             = "~1.44", "good",         2
    P3             = "~1.73", "great",        3
    P4             = "~2.07", "excellent",    4
    P5             = "~2.49", "superior",     5
    P6             = "~2.99", "amazing",      6
    P7             = "~3.58", "exceptional",  7
    P8             = "~4.30", "incredible",   8
    P9             = "~5.16", "phenomenal",   9

    def __init__(self, approximation: str, adjective: str, power: float) -> None:
        self.approximation = approximation
        self.adjective = adjective
        self.power = power
        self.mod: float
        if power == -inf:
            self.mod = 0
        elif power < 0:
            self.mod = 1.25 ** power
        else:
            self.mod = 1.2 ** power

    @property
    def adjective_capitalized(self) -> str:
        return self.adjective.capitalize()
