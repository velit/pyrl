from __future__ import annotations

from collections.abc import Sequence

from pyrl.config.binds import Binds
from pyrl.creature.inventory import Inventory
from pyrl.engine.actions.action import Action
from pyrl.engine.actions.action_exceptions import NoValidTargetException
from pyrl.engine.actions.action_feedback import ActionFeedback, NoActionFeedback
from pyrl.engine.actions.action_interface import ActionInterface
from pyrl.creature.equipment_slot import Slot
from pyrl.user_interface.line import Line
from pyrl.user_interface.lines_view import lines_view, multi_select_lines_view

def _get_equipment_item_str(inventory: Inventory, slot: Slot) -> str:
    item = inventory.get_item(slot)
    if item is None:
        return "-"
    if not item.uses_all_slots or slot == item.compatible_slots[0]:
        return str(item)
    else:
        return item.name

def equipment_view(actions: ActionInterface) -> ActionFeedback:
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
            return NoActionFeedback
        elif key in Binds.Equipment_View_Backpack:
            feedback = backpack_view(actions)
            if feedback.action != Action.No_Action:
                return feedback
        elif slot is not None and slot in Slot:
            if inventory.get_item(slot) is None:
                backpack_equip_item_view(actions, slot)
            else:
                inventory.unequip(slot)
        else:
            assert False, f"Got unhandled return values {key=} {slot=}"

def backpack_equip_item_view(actions: ActionInterface, slot: Slot) -> None:
    lines: Sequence[Line[int]] = tuple(Line(str(item), i) for i, item in enumerate(actions.inspect_character_items())
                                       if item.fits_slot(slot))
    key, item = lines_view(actions.io.whole_window, lines, select_keys=Binds.Backpack_Select_Keys,
                           header="Select item to equip")
    if key in Binds.Cancel:
        return
    elif item is not None:
        actions.player.inventory.equip_from_bag(item, slot)

def backpack_view(actions: ActionInterface) -> ActionFeedback:
    lines: Sequence[Line[int]] = tuple(Line(str(item), i) for i, item in enumerate(actions.inspect_character_items()))
    header = f"Backpack (Press {Binds.Backpack_Drop_Items.key} to drop selected items)"
    key, selections = multi_select_lines_view(actions.io.whole_window, lines,
                                              select_keys=Binds.Backpack_Select_Keys,
                                              return_keys=Binds.Backpack_Drop_Items + Binds.Cancel,
                                              header=header)
    if key in Binds.Backpack_Drop_Items:
        return actions.drop_items(selections)
    return NoActionFeedback

def pickup_items_view(actions: ActionInterface) -> ActionFeedback:

    lines: Sequence[Line[int]] = tuple(Line(str(item), i) for i, item in enumerate(actions.inspect_floor_items()))
    if not lines:
        raise NoValidTargetException("Creature tried to pick up items in a place without any.",
                                     "There aren't any items here to pick up.")
    elif len(lines) == 1:
        return actions.pickup_items((lines[0].return_value, ))

    key, selections = multi_select_lines_view(actions.io.whole_window, lines,
                                              select_keys=Binds.Backpack_Select_Keys,
                                              header="Select items to pick up")
    if key in Binds.Cancel and selections:
        return actions.pickup_items(selections)
    return NoActionFeedback

def drop_items_view(actions: ActionInterface) -> ActionFeedback:
    lines: Sequence[Line[int]] = tuple(Line(str(item), i) for i, item in enumerate(actions.inspect_character_items()))
    key, selections = multi_select_lines_view(actions.io.whole_window, lines,
                                              select_keys=Binds.Backpack_Select_Keys,
                                              header="Select items to drop")
    if key in Binds.Cancel and selections:
        return actions.drop_items(selections)
    return NoActionFeedback
