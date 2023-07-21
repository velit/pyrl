from typing import Callable

from pyrl.engine.creature.mixins.learner import Learner
from pyrl.engine.types.glyphs import Glyph, GreenAt

class ConcreteLearner(Learner):

    @property
    def name(self) -> str:
        return "Learner"

    @property
    def glyph(self) -> Glyph:
        return GreenAt

def test_learner() -> None:
    level_xp_unit = 1000
    next_level_limit: Callable[[int], int] = lambda lvl: Learner.calc_next_level_limit(lvl, level_xp_unit)
    xp_level: Callable[[int], int] = lambda xp: Learner.calc_experience_level(xp, level_xp_unit)

    for level in range(100):
        assert level == xp_level(next_level_limit(level)) - 1

    limits = {
        0:  500,     1:  1000,    2:  2500,    3:  5000,    4:  8500,
        5:  13000,   6:  18500,   7:  25000,   8:  32500,   9:  41000,
        10: 50500,   11: 61000,   12: 72500,   13: 85000,   14: 98500,
        15: 113000,  16: 128500,  17: 145000,  18: 162500,  19: 181000,
        20: 200500,  21: 221000,  22: 242500,  23: 265000,  24: 288500,
        25: 313000,  26: 338500,  27: 365000,  28: 392500,  29: 421000,
        30: 450500,  31: 481000,  32: 512500,  33: 545000,  34: 578500,
        35: 613000,  36: 648500,  37: 685000,  38: 722500,  39: 761000,
        40: 800500,  41: 841000,  42: 882500,  43: 925000,  44: 968500,
        45: 1013000, 46: 1058500, 47: 1105000, 48: 1152500, 49: 1201000,
        50: 1250500, 51: 1301000, 52: 1352500, 53: 1405000, 54: 1458500,
        55: 1513000, 56: 1568500, 57: 1625000, 58: 1682500, 59: 1741000,
        60: 1800500, 61: 1861000, 62: 1922500, 63: 1985000, 64: 2048500,
        65: 2113000, 66: 2178500, 67: 2245000, 68: 2312500, 69: 2381000,
        70: 2450500, 71: 2521000, 72: 2592500, 73: 2665000, 74: 2738500,
        75: 2813000, 76: 2888500, 77: 2965000, 78: 3042500, 79: 3121000,
        80: 3200500, 81: 3281000, 82: 3362500, 83: 3445000, 84: 3528500,
        85: 3613000, 86: 3698500, 87: 3785000, 88: 3872500, 89: 3961000,
        90: 4050500, 91: 4141000, 92: 4232500, 93: 4325000, 94: 4418500,
        95: 4513000, 96: 4608500, 97: 4705000, 98: 4802500, 99: 4901000
    }

    for level, limit in limits.items():
        assert next_level_limit(level) == limit
        assert level == xp_level(limit) - 1

    learner = ConcreteLearner()
    learner.gain_xp(limits[97])
    assert learner.creature_level == 98
    learner.gain_xp(limits[98] - limits[97])
    assert learner.creature_level == 99
