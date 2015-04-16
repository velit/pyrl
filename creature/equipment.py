from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum
from .stats import Stat


class Slot(Enum):

    head       = "Head"
    body       = "Body"
    right_hand = "Right Hand"
    left_hand  = "Left Hand"
    feet       = "Feet"


class Equipment(object):

    def __init__(self):

        self.stats = {stat: 0 for stat in Stat}

        self.items = {
            Slot.head:        None,
            Slot.body:        None,
            Slot.right_hand:  None,
            Slot.left_hand:   None,
            Slot.feet:        None,
        }

    def equip(self, slot, item):
        if self.items[slot] is not None:
            assert False
        self.items[slot] = item
        self.add_item_stats(item)

    def unequip(self, slot):
        item = self.items[slot]
        if self.items[slot] is None:
            assert False
        self.items[slot] = None
        self.remove_item_stats(item)

    def add_item_stats(self, item):
        for stat, value in item.stats:
            self.stats[stat] += value

    def remove_item_stats(self, item):
        for stat, value in item.stats:
            self.stats[stat] -= value

    def get_damage_info(self):
        if self.items[Slot.right_hand] is not None:
            return self.items[Slot.right_hand].get_damage()
        elif self.items[Slot.left_hand] is not None:
            return self.items[Slot.left_hand].get_damage()
        else:
            return None
