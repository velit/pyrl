from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum
from creature.stats import Stat


class Slot(Enum):

    Head       = "Head"
    Body       = "Body"
    Right_Hand = "Right Hand"
    Left_Hand  = "Left Hand"
    Feet       = "Feet"


class Equipment(object):

    def __init__(self):

        self.applied_stats = {stat: 0 for stat in Stat}

        self._bag = []
        self._worn_items = {
            Slot.Head:        None,
            Slot.Body:        None,
            Slot.Right_Hand:  None,
            Slot.Left_Hand:   None,
            Slot.Feet:        None,
        }

    def get_item(self, slot):
        return self._worn_items[slot]

    def equip_from_bag(self, index, slot):
        item = self.unbag_item(index)
        self.equip(item, slot)

    def equip(self, item, slot):
        assert slot in item.compatible_slots, "Item {} does not fit into slot {}".format(item, slot)

        if self._worn_items[slot] is not None:
            self.unequip(slot)
        self._worn_items[slot] = item
        self._add_stats(item)

    def unequip(self, slot):
        assert self._worn_items[slot] is not None, "Slot is already empty"

        item = self._worn_items[slot]
        self._worn_items[slot] = None
        self._remove_stats(item)
        self.bag_item(item)

    def bag_item(self, item):
        self._bag.append(item)

    def bag_items(self, items):
        self._bag.extend(items)

    def unbag_item(self, item_index):
        return self._bag.pop(item_index)

    def unbag_items(self, item_indexes):
        index_set = tuple(item_indexes)
        unbagged_items = tuple(self._bag[index] for index in item_indexes)
        self._bag = [item for index, item in enumerate(self._bag) if index not in index_set]
        return unbagged_items

    def get_damage_info(self):
        if self._worn_items[Slot.Right_Hand] is not None:
            return self._worn_items[Slot.Right_Hand].get_damage()
        elif self._worn_items[Slot.Left_Hand] is not None:
            return self._worn_items[Slot.Left_Hand].get_damage()
        else:
            return None

    def view_items(self):
        return tuple(self._bag)

    def _add_stats(self, item):
        for stat, value in item.stats:
            self.applied_stats[stat] += value

    def _remove_stats(self, item):
        for stat, value in item.stats:
            self.applied_stats[stat] -= value
