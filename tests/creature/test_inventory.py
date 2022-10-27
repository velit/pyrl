from __future__ import annotations

import dataclasses

from pyrl.creature.equipment_slot import Slot
from pyrl.creature.inventory import Inventory
from pyrl.creature.item import Weapon, Armor
from pyrl.creature.stats import Stats
from pyrl.structures.dice import Dice

def test_creature_inventory() -> None:
    inventory = Inventory()
    test_equipment = {
        Slot.Right_Hand: Weapon("short sword +1", 0, Dice(1, 6, 1)),
        Slot.Left_Hand:  Weapon("short sword", 0, Dice(1, 6, 0)),
        Slot.Head:       Armor("helmet", 0, 1, [Slot.Head]),
        Slot.Body:       Armor("armor", 0, 4, [Slot.Body], stats=Stats(strength=2)),
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
    assert inventory.stats.armor == 6
    assert inventory.stats.strength == 2

    # unequip items
    for slot in test_equipment:
        inventory.unequip(slot)

    assert len(inventory._bag) == len(test_equipment)

    two_hander = Weapon("two-handed sword", 0, Dice(1, 6, 0), two_handed=True)
    inventory.equip(two_hander, two_hander.compatible_slots[0])
    inventory.unequip(two_hander.compatible_slots[1])

    for worn_item in inventory._equipment.values():
        assert worn_item is None

    for stat_value in dataclasses.astuple(inventory.stats):
        assert stat_value == 0
