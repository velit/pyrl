from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from pyrl.config.binds import Binds
from pyrl.types.equipment_slot import Slot
from pyrl.creature.game_actions import GameActions
from pyrl.creature.action import Action, NoValidTargetException
from pyrl.creature.inventory import Inventory
from pyrl.user_interface.lines_view import lines_view, multi_select_lines_view
from pyrl.types.line import Line

def _get_equipment_item_str(inventory: Inventory, slot: Slot) -> str:
    item = inventory.get_item(slot)
    if item is None:
        return "-"
    if not item.uses_all_slots or slot == item.compatible_slots[0]:
        return str(item)
    else:
        return item.name

def equipment_view(actions: GameActions) -> Literal[Action.No_Action, Action.Drop_Items]:
    footer = f"Press a slot key to (un)equip" \
             f"  {Binds.Equipment_View_Backpack.key} to view backpack" \
             f"  {Binds.Cancel.key} to close"
    inventory: Inventory = actions.player.inventory

    while True:
        lines: Sequence[Line[Slot]] = tuple(Line(f"{slot.value:11}: {_get_equipment_item_str(inventory, slot)}", slot)
                                            for slot in Slot)
        key, slot = lines_view(actions.io.whole_window, lines, select_keys=Binds.EquipmentSelectKeys,
                               return_keys=Binds.Equipment_View_Backpack + Binds.Cancel, header="Equipment",
                               footer=footer)

        if key in Binds.Cancel:
            return Action.No_Action
        elif key in Binds.Equipment_View_Backpack:
            action = backpack_view(actions)
            if action != Action.No_Action:
                return action
        elif slot is not None and slot in Slot:
            if inventory.get_item(slot) is None:
                backpack_equip_item_view(actions, slot)
            else:
                inventory.unequip(slot)
        else:
            assert False, f"Got unhandled return values {key=} {slot=}"

def backpack_equip_item_view(actions: GameActions, slot: Slot) -> None:
    lines: Sequence[Line[int]] = tuple(Line(str(item), i) for i, item in enumerate(actions.inspect_character_items())
                                       if item.fits_slot(slot))
    key, item = lines_view(actions.io.whole_window, lines, select_keys=Binds.Backpack_Select_Keys,
                           header="Select item to equip")
    if key in Binds.Cancel:
        return
    elif item is not None:
        actions.player.inventory.equip_from_bag(item, slot)

def backpack_view(actions: GameActions) -> Literal[Action.Drop_Items, Action.No_Action]:
    lines: Sequence[Line[int]] = tuple(Line(str(item), i) for i, item in enumerate(actions.inspect_character_items()))
    header = f"Backpack (Press {Binds.Backpack_Drop_Items.key} to drop selected items)"
    key, selections = multi_select_lines_view(actions.io.whole_window, lines,
                                              select_keys=Binds.Backpack_Select_Keys,
                                              return_keys=Binds.Backpack_Drop_Items + Binds.Cancel,
                                              header=header)
    if key in Binds.Backpack_Drop_Items:
        action, item_description = actions.drop_items(selections)
        actions.io.msg(f"Dropped {item_description}")
        return action
    return Action.No_Action

def pickup_items_view(actions: GameActions) -> Literal[Action.Pick_Items, Action.No_Action]:

    lines: Sequence[Line[int]] = tuple(Line(str(item), i) for i, item in enumerate(actions.inspect_floor_items()))
    if not lines:
        raise NoValidTargetException("Creature tried to pick up items in a place without any.",
                                     "There aren't any items here to pick up.")
    elif len(lines) == 1:
        action, item_description = actions.pickup_items((lines[0].return_value, ))
        actions.io.msg(f"Picked up {item_description}")
        return action

    key, selections = multi_select_lines_view(actions.io.whole_window, lines,
                                              select_keys=Binds.Backpack_Select_Keys,
                                              header="Select items to pick up")
    if key in Binds.Cancel and selections:
        action, item_description = actions.pickup_items(selections)
        actions.io.msg(f"Picked up {item_description}")
        return action
    return Action.No_Action

def drop_items_view(actions: GameActions) -> Literal[Action.Drop_Items, Action.No_Action]:
    lines: Sequence[Line[int]] = tuple(Line(str(item), i) for i, item in enumerate(actions.inspect_character_items()))
    key, selections = multi_select_lines_view(actions.io.whole_window, lines,
                                              select_keys=Binds.Backpack_Select_Keys,
                                              header="Select items to drop")
    if key in Binds.Cancel and selections:
        action, item_description = actions.drop_items(selections)
        actions.io.msg(f"Dropped {item_description}")
        return action
    return Action.No_Action
