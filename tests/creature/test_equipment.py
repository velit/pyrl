from __future__ import annotations

import dataclasses

from pyrl.constants.equipment_slot import Slot
from pyrl.creature.inventory import Inventory
from pyrl.creature.item import Weapon, Armor
from pyrl.creature.stats import Stats
from pyrl.dice import Dice

def test_creature_equipment():
    equipment = Inventory()
    items = {
        Slot.Right_Hand: Weapon("short sword +1", 0, Dice(1, 6, 1)),
        Slot.Left_Hand:  Weapon("short sword", 0, Dice(1, 6, 0)),
        Slot.Head:       Armor("helmet", 0, 1, [Slot.Head]),
        Slot.Body:       Armor("armor", 0, 4, [Slot.Body], stats=Stats(strength=2)),
        Slot.Feet:       Armor("boots", 0, 1, [Slot.Feet]),
    }

    # bag items
    equipment.bag_items(items.values())
    for item in items.values():
        assert item in equipment._bag

    assert len(equipment._bag) == len(items)

    # equip items
    for slot, item in items.items():
        equipment.equip_from_bag(equipment._bag.index(item), slot)
        assert equipment.get_item(slot) is item

    assert len(equipment._bag) == 0
    assert equipment.stats.armor == 6
    assert equipment.stats.strength == 2

    # unequip items
    for slot in items:
        equipment.unequip(slot)

    assert len(equipment._bag) == len(items)

    two_hander = Weapon("two-handed sword", 0, Dice(1, 6, 0), two_handed=True)
    equipment.equip(two_hander, two_hander.compatible_slots[0])
    equipment.unequip(two_hander.compatible_slots[1])

    for worn_item in equipment._equipment.values():
        assert worn_item is None

    for stat_value in dataclasses.astuple(equipment.stats):
        assert stat_value == 0
