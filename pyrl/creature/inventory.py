from __future__ import annotations

from collections.abc import Iterable
from dataclasses import field, dataclass

from pyrl.creature.item import Item
from pyrl.creature.stats import Stats
from pyrl.structures.dice import Dice
from pyrl.types.equipment_slot import Slot

@dataclass(eq=False)
class Inventory:

    stats: Stats = field(init=False, default_factory=Stats)
    _equipment: dict[Slot, Item | None] = field(init=False, default_factory=lambda: {
        Slot.Head:       None,
        Slot.Body:       None,
        Slot.Right_Hand: None,
        Slot.Left_Hand:  None,
        Slot.Feet:       None,
    })
    _bag: list[Item] = field(init=False, default_factory=list)

    @property
    def damage_dice(self) -> Dice | None:
        right_hand = self._equipment[Slot.Right_Hand]
        left_hand = self._equipment[Slot.Left_Hand]
        if right_hand and right_hand.damage_dice:
            return right_hand.damage_dice
        elif left_hand and left_hand.damage_dice:
            return left_hand.damage_dice
        else:
            return None

    def get_item(self, slot: Slot) -> Item | None:
        return self._equipment[slot]

    def equip_from_bag(self, index: int, slot: Slot) -> None:
        item = self.unbag_item(index)
        self.equip(item, slot)

    def equip(self, item: Item, select_slot: Slot) -> None:
        assert select_slot in item.compatible_slots, \
            f"{item=} does not fit into {select_slot=}"

        if item.uses_all_slots:
            equip_slots = item.compatible_slots
        else:
            equip_slots = (select_slot, )

        for slot in equip_slots:
            if self._equipment[slot] is not None:
                self.unequip(slot)
            self._equipment[slot] = item
        self._update_combined_stats()

    def unequip(self, select_slot: Slot) -> None:
        item = self._equipment[select_slot]
        assert item is not None, "Slot is already empty"

        if item.uses_all_slots:
            unequip_slots = item.compatible_slots
        else:
            unequip_slots = (select_slot, )

        for slot in unequip_slots:
            self._equipment[slot] = None

        self.bag_item(item)
        self._update_combined_stats()

    def bag_item(self, item: Item) -> None:
        self._bag.append(item)

    def bag_items(self, items: Iterable[Item]) -> None:
        self._bag.extend(items)

    def unbag_item(self, item_index: int) -> Item:
        return self._bag.pop(item_index)

    def unbag_items(self, item_indexes: Iterable[int]) -> tuple[Item, ...]:
        index_set = tuple(item_indexes)
        unbagged_items = tuple(self._bag[index] for index in item_indexes)
        self._bag = [item for index, item in enumerate(self._bag) if index not in index_set]
        return unbagged_items

    def inspect_items(self) -> tuple[Item, ...]:
        return tuple(self._bag)

    def _update_combined_stats(self) -> None:
        self.stats = Stats.combine(*(item.stats for item in self._equipment.values() if item))

    def __repr__(self) -> str:
        return str(self._equipment)
