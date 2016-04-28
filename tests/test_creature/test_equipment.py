import pytest

from creature.equipment import Equipment, Slot
from creature.item import Item, Weapon
from creature.stats import Stat


@pytest.fixture
def equipment():
    return Equipment()


@pytest.fixture
def items():
    return {
        Slot.Right_Hand: Weapon("short sword +1", (1, 6, 1)),
        Slot.Left_Hand:  Weapon("short sword", (1, 6, 0)),
        Slot.Head:       Item("helmet", [Slot.Head]).add_stat(Stat.armor, 1),
        Slot.Body:       Item("armor", [Slot.Body], stats=[(Stat.strength, 2), (Stat.armor, 4)]),
        Slot.Feet:       Item("boots", [Slot.Feet]).add_stat(Stat.armor, 1),
    }


def test_creature_equipment(equipment, items):

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
    assert equipment.applied_stats[Stat.armor] == 6
    assert equipment.applied_stats[Stat.strength] == 2

    # unequip items
    for slot in items:
        equipment.unequip(slot)

    # final checks
    assert len(equipment._bag) == len(items)

    for worn_item in equipment._worn_items.values():
        assert worn_item is None

    for stat_value in equipment.applied_stats.values():
        assert stat_value == 0
