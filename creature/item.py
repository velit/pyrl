from __future__ import absolute_import, division, print_function, unicode_literals

from dice import Dice
from .equipment import Slot


def get_stats_str(stats):
    stats_str = ", ".join("{0}:{1}".format(stat.value, value) for stat, value in stats)
    return "{" + stats_str + "}"


class Item(object):
    def __init__(self, name, stats=(), compatible_slots=()):
        self.name = name
        self.stats = tuple(stats)
        self.compatible_slots = tuple(compatible_slots)

    def __str__(self):
        if self.stats:
            stats_str = get_stats_str(self.stats)
            return "{0.name} {1}".format(self, stats_str)
        else:
            return "{0.name}".format(self)

    def add_stat(self, stat, value):
        self.stats += ((stat, value), )
        return self

    def fits_to_slot(self, slot):
        return slot in self.compatible_slots

    def __lt__(self, other):
        return str(self) < str(other)


class Weapon(Item):
    def __init__(self, name, dice, sides, addition, stats=(),
                 compatible_slots=(Slot.right_hand, Slot.left_hand)):
        super().__init__(name, stats, compatible_slots)
        self.damage = Dice(dice, sides, addition)

    def roll(self):
        return self.damage.roll()

    def get_damage(self):
        return self.damage.get_values()

    def __str__(self):
        if self.stats:
            stats_str = get_stats_str(self.stats)
            return "{0.name} ({0.damage}) {1}".format(self, stats_str)
        else:
            return "{0.name} ({0.damage})".format(self)
