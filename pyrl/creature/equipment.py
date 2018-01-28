from pyrl.enums.slot import Slot
from pyrl.creature.stats import Stat, ComplexStat


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

    def _set_items(self, slots, value):
        for slot in slots:
            self._worn_items[slot] = value

    def equip(self, item, select_slot):
        assert select_slot in item.compatible_slots, \
            "Item {} does not fit into slot {}".format(item, select_slot)

        if item.occupies_all_slots:
            equip_slots = item.compatible_slots
        else:
            equip_slots = (select_slot, )

        for slot in equip_slots:
            if self._worn_items[slot] is not None:
                self.unequip(slot)
            self._worn_items[slot] = item
        self._add_stats(item)

    def unequip(self, select_slot):
        assert self._worn_items[select_slot] is not None, "Slot is already empty"

        item = self._worn_items[select_slot]
        if item.occupies_all_slots:
            unequip_slots = item.compatible_slots
        else:
            unequip_slots = (select_slot, )

        for slot in unequip_slots:
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
        right_hand = self._worn_items[Slot.Right_Hand]
        left_hand = self._worn_items[Slot.Left_Hand]
        if right_hand is not None and right_hand.get_stat(ComplexStat.weapon_dice) is not None:
            return right_hand.get_stat(ComplexStat.weapon_dice)
        elif left_hand is not None and left_hand.get_stat(ComplexStat.weapon_dice) is not None:
            return left_hand.get_stat(ComplexStat.weapon_dice)
        else:
            return None

    def view_items(self):
        return tuple(self._bag)

    def _add_stats(self, item):
        for stat, value in item.stats:
            if stat in Stat:
                self.applied_stats[stat] += value

    def _remove_stats(self, item):
        for stat, value in item.stats:
            if stat in Stat:
                self.applied_stats[stat] -= value

    def __repr__(self):
        return str(self._worn_items)
