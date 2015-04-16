from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
from creature.equipment import Equipment, Slot
from creature.stats import Stat
from creature.item import Item, Weapon


@pytest.fixture
def equipment():
    return Equipment()


@pytest.fixture
def items():
    items_ = {
        Slot.right_hand: Weapon("short sword +1", 1, 6, 1),
        Slot.left_hand:  Weapon("short sword", 1, 6, 0),
        Slot.head:       Item("helmet", [(Stat.armor, 1)], [Slot.head]),
        Slot.body:       Item("armor", [(Stat.strength, 2), (Stat.armor, 4)], [Slot.body]),
        Slot.feet:       Item("boots", [(Stat.armor, 1)], [Slot.feet]),
    }
    return items_


def test_equipment(equipment, items):

    # bag items
    for item in items.values():
        equipment.bag_item(item)
        assert item in equipment.bag_of_holding

    assert len(equipment.bag_of_holding) == len(items)

    # equip items
    for slot, item in items.items():
        equipment.equip(item, slot)
        assert equipment.get_item(slot) is item

    assert len(equipment.bag_of_holding) == 0
    assert equipment.applied_stats[Stat.armor] == 6
    assert equipment.applied_stats[Stat.strength] == 2

    # unequip items
    for slot in items:
        equipment.unequip(slot)

    # final checks
    assert len(equipment.bag_of_holding) == len(items)
    for worn_item in equipment.worn_items.values():
        assert worn_item is None

    for stat_value in equipment.applied_stats.values():
        assert stat_value == 0
