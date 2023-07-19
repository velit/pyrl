from typing import Callable

from pyrl.engine.creature.mixins.learner import Learner
from pyrl.engine.types.glyphs import Colors

def test_learner() -> None:
    level_xp_unit = 1000
    xp_limit: Callable[[int], int] = lambda lvl: Learner.calc_experience_limit(lvl, level_xp_unit)
    xp_level: Callable[[int], int] = lambda xp: Learner.calc_experience_level(xp, level_xp_unit)

    for level in range(1, 101):
        assert level + 1 == xp_level(xp_limit(level))

    limits = {1:  500, 2: 1000, 3: 2500, 4: 5000, 5: 8500, 6: 13000, 7: 18500, 8: 25000, 9: 32500, 10: 41000, 11: 50500,
              12: 61000, 13: 72500, 14: 85000, 15: 98500, 16: 113000, 17: 128500, 18: 145000, 19: 162500, 20: 181000,
              21: 200500, 22: 221000, 23: 242500, 24: 265000, 25: 288500, 26: 313000, 27: 338500, 28: 365000,
              29: 392500, 30: 421000, 31: 450500, 32: 481000, 33: 512500, 34: 545000, 35: 578500, 36: 613000,
              37: 648500, 38: 685000, 39: 722500, 40: 761000, 41: 800500, 42: 841000, 43: 882500, 44: 925000,
              45: 968500, 46: 1013000, 47: 1058500, 48: 1105000, 49: 1152500, 50: 1201000, 51: 1250500, 52: 1301000,
              53: 1352500, 54: 1405000, 55: 1458500, 56: 1513000, 57: 1568500, 58: 1625000, 59: 1682500, 60: 1741000,
              61: 1800500, 62: 1861000, 63: 1922500, 64: 1985000, 65: 2048500, 66: 2113000, 67: 2178500, 68: 2245000,
              69: 2312500, 70: 2381000, 71: 2450500, 72: 2521000, 73: 2592500, 74: 2665000, 75: 2738500, 76: 2813000,
              77: 2888500, 78: 2965000, 79: 3042500, 80: 3121000, 81: 3200500, 82: 3281000, 83: 3362500, 84: 3445000,
              85: 3528500, 86: 3613000, 87: 3698500, 88: 3785000, 89: 3872500, 90: 3961000, 91: 4050500, 92: 4141000,
              93: 4232500, 94: 4325000, 95: 4418500, 96: 4513000, 97: 4608500, 98: 4705000}

    for level, limit in limits.items():
        assert xp_limit(level) == limit
        assert level + 1 == xp_level(limit)

    learner = Learner("test", ("t", Colors.Green), 0)
    learner.gain_xp(limits[97])
    assert learner.creature_level == 98
    learner.gain_xp(limits[98] - limits[97])
    assert learner.creature_level == 99
