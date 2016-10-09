from bindings import Bind
from creature.equipment import Slot
from game_actions import ActionError, feedback
from interface.lines_view import lines_view, Line


def _get_equipment_item_str(equipment, slot):
    item = equipment.get_item(slot)
    if item is None:
        return "-"
    if not item.occupies_all_slots or slot == item.compatible_slots[0]:
        return str(item)
    else:
        return "{}".format(item.name)


def equipment(actions):
    footer_fmt = "Press a slot key to (un)equip  {} to view backpack  {} to close"
    footer = footer_fmt.format(Bind.Equipment_View_Backpack.key, Bind.Cancel.key)
    equipment = actions.creature.equipment

    while True:
        lines = tuple(Line("{:11}: {}".format(slot.value, _get_equipment_item_str(equipment, slot)), slot)
                      for slot in Slot)
        key, slot = lines_view(actions.io.whole_window, lines,
                               multi_select=False,
                               select_keys=Bind.Equipment_Select_Keys,
                               return_keys=Bind.Equipment_View_Backpack + Bind.Cancel,
                               header="Equipment",
                               footer=footer)

        if key in Bind.Cancel:
            return
        elif key in Bind.Equipment_View_Backpack:
            backpack(actions)
        elif slot in Slot:
            if equipment.get_item(slot) is None:
                backpack_equip_item(actions, slot)
            else:
                equipment.unequip(slot)
        else:
            assert False, "Got unhandled return values, key: {} value: {}".format(key, slot)


def backpack_equip_item(actions, slot):
    lines = tuple(Line(str(item), i) for i, item in enumerate(actions.view_character_items())
                  if item.fits_slot(slot))
    key, item = lines_view(actions.io.whole_window, lines, select_keys=Bind.Backpack_Select_Keys,
                        header="Select item to equip")
    if key in Bind.Cancel:
        return
    else:
        actions.creature.equipment.equip_from_bag(item, slot)


def backpack(actions):
    lines = tuple(Line(str(item), i) for i, item in enumerate(actions.view_character_items()))
    key, selections = lines_view(
        actions.io.whole_window,
        lines,
        multi_select=True,
        select_keys=Bind.Backpack_Select_Keys,
        return_keys=Bind.Backpack_Drop_Items + Bind.Cancel,
        header="Backpack".format(Bind.Backpack_Drop_Items.key),
    )
    if key in Bind.Cancel:
        return
    elif key in Bind.Backpack_Drop_Items:
        return actions.drop_items(selections)


def pickup_items(actions):
    lines = tuple(Line(str(item), i) for i, item in enumerate(actions.view_floor_items()))

    if not lines:
        return feedback(ActionError.NoItemsOnGround)
    elif len(lines) == 1:
        return actions.pickup_items((lines[0][0], ))

    key, selections = lines_view(
        actions.io.whole_window,
        lines,
        multi_select=True,
        select_keys=Bind.Backpack_Select_Keys,
        header="Select items to pick up"
    )
    if key in Bind.Cancel and selections:
        return actions.pickup_items(selections)


def drop_items(actions):
    lines = tuple(Line(str(item), i) for i, item in enumerate(actions.view_character_items()))
    key, selections = lines_view(
        actions.io.whole_window,
        lines,
        multi_select=True,
        select_keys=Bind.Backpack_Select_Keys,
        header="Select items to drop".format(Bind.Backpack_Drop_Items.key)
    )
    if key in Bind.Cancel and selections:
        return actions.drop_items(selections)
