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

        self.applied_stats = {stat: 0 for stat in Stat}

        self.bag_of_holding = set()
        self.worn_items = {
            Slot.head:        None,
            Slot.body:        None,
            Slot.right_hand:  None,
            Slot.left_hand:   None,
            Slot.feet:        None,
        }

    def get_item(self, slot):
        return self.worn_items[slot]

    def equip(self, item, slot):
        if slot not in item.compatible_slots:
            raise AssertionError("Item {} does not fit into slot {}".format(item, slot))
        self.unbag_item(item)
        if self.worn_items[slot] is not None:
            self.unequip(slot)
        self._equip_item(item, slot)

    def unequip(self, slot):
        item = self.worn_items[slot]
        if self.worn_items[slot] is None:
            raise AssertionError("Slot is already empty")
        self._unequip_item(item, slot)
        self.bag_item(item)

    def bag_item(self, item):
        self.bag_of_holding.add(item)

    def unbag_item(self, item):
        self.bag_of_holding.remove(item)

    def get_damage_info(self):
        if self.worn_items[Slot.right_hand] is not None:
            return self.worn_items[Slot.right_hand].get_damage()
        elif self.worn_items[Slot.left_hand] is not None:
            return self.worn_items[Slot.left_hand].get_damage()
        else:
            return None

    def get_inventory_lines(self):
        f = "{1}. {0.name} {0.stats}"
        for i, item in enumerate(self.bag_of_holding):
            yield f.format(item, (i + 1) % 10)

    def get_inventory_items(self, slot=None):
        """Return a sorted tuple of inventory items in given slot, if None return all items."""
        if slot is not None:
            return tuple(sorted(item for item in self.bag_of_holding if item.fits_to_slot(slot)))
        else:
            return tuple(sorted(self.bag_of_holding))

    def _equip_item(self, item, slot):
        self.worn_items[slot] = item
        for stat, value in item.stats:
            self.applied_stats[stat] += value

    def _unequip_item(self, item, slot):
        self.worn_items[slot] = None
        for stat, value in item.stats:
            self.applied_stats[stat] -= value
