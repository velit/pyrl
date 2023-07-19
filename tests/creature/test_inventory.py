from __future__ import annotations

import dataclasses
from collections import Counter

from pyrl.engine.creature.inventory import Inventory
from pyrl.engine.creature.item import Weapon, Armor, Slot
from pyrl.engine.creature.stats import Stats, Stat
from pyrl.engine.structures.dice import Dice

def test_creature_inventory() -> None:
    stats_changed_count = "stats_changed_count"
    state = {stats_changed_count: 0}

    def stats_changed_event() -> None:
        state[stats_changed_count] += 1

    inventory = Inventory(stats_changed_event)
    test_equipment = {
        Slot.Right_Hand: Weapon("short sword +1", 0, Dice(1, 6, 1)),
        Slot.Left_Hand:  Weapon("short sword", 0, Dice(1, 6, 0)),
        Slot.Head:       Armor("helmet", 0, 1, [Slot.Head]),
        Slot.Body:       Armor("armor", 0, 4, [Slot.Body], stats=Stats({Stat.STR: 2})),
        Slot.Feet:       Armor("boots", 0, 1, [Slot.Feet]),
    }

    # bag items
    inventory.bag_items(test_equipment.values())
    for item in test_equipment.values():
        assert item in inventory._bag

    assert len(inventory._bag) == len(test_equipment)

    # equip items
    for slot, item in test_equipment.items():
        inventory.equip_from_bag(inventory._bag.index(item), slot)
        assert inventory.get_item(slot) is item

    assert len(inventory._bag) == 0
    assert state[stats_changed_count] == 5
    assert len(list(inventory.stats_sources())) == 5

    # unequip items
    for slot in test_equipment:
        inventory.unequip(slot)

    assert len(inventory._bag) == len(test_equipment)

    assert state[stats_changed_count] == 10
    assert len(list(inventory.stats_sources())) == 0

    two_hander = Weapon("two-handed sword", 0, Dice(1, 6, 0), two_handed=True)
    inventory.equip(two_hander, two_hander.compatible_slots[0])
    inventory.unequip(two_hander.compatible_slots[1])

    for worn_item in inventory._equipment.values():
        assert worn_item is None

    assert len(list(inventory.stats_sources())) == 0
