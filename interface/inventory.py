from __future__ import absolute_import, division, print_function, unicode_literals

from interface.lines_view import lines_view, multi_select_lines_view
from config.bindings import Bind
from creature.equipment import Slot
from collections import namedtuple

EquipmentRow = namedtuple('EquipmentRow', ('key', 'slot'))
equipment_rows = (
    EquipmentRow(Bind.Equipment_Slot_Head.key,       Slot.head),
    EquipmentRow(Bind.Equipment_Slot_Body.key,       Slot.body),
    EquipmentRow(Bind.Equipment_Slot_Right_Hand.key, Slot.right_hand),
    EquipmentRow(Bind.Equipment_Slot_Left_Hand.key,  Slot.left_hand),
    EquipmentRow(Bind.Equipment_Slot_Feet.key,       Slot.feet),
)


def equipment(io, char_equipment):
    select_keys = tuple(row.key for row in equipment_rows)
    return_keys = Bind.View_Inventory
    header = "Equipment"
    footer_fmt = "Press a slot key to (un)equip  {} to view backpack  {} to close"
    footer = footer_fmt.format(Bind.View_Inventory.key, Bind.Cancel.key)

    while True:
        lines = ("{0:11}: {1}".format(row.slot.value, char_equipment.get_item(row.slot)) for row in equipment_rows)
        retval = lines_view(io.whole_window, lines, select_keys, return_keys, header, footer)

        if retval is None:
            return
        elif retval in Bind.View_Inventory:
            backpack(io, char_equipment)
        elif retval in range(len(equipment_rows)):
            slot = equipment_rows[retval].slot
            if char_equipment.get_item(slot) is None:
                equip_item = backpack_equip_item(io, char_equipment, slot)
                if equip_item is not None:
                    char_equipment.equip(equip_item, slot)
            else:
                char_equipment.unequip(slot)
        else:
            assert False, "Got unhandled return value as input {}".format(retval)


def backpack_equip_item(io, char_equipment, slot):

    items = char_equipment.get_inventory_items(slot)
    lines = (str(item) for item in items)

    header = "Select item to equip"
    index = lines_view(io.whole_window, lines, select_keys=Bind.Item_Select_Keys,
                        header=header)
    if index is not None:
        return items[index]
    else:
        return None


def backpack(io, char_equipment):

    items = char_equipment.get_inventory_items()
    lines = tuple(str(item) for item in items)

    header = "Backpack"
    key, selected_item_indexes = multi_select_lines_view(io.whole_window, lines,
                                                   select_keys=Bind.Item_Select_Keys, header=header)
    if selected_item_indexes:
        selected_lines = (lines[i] for i in selected_item_indexes)
        for description in selected_lines:
            io.msg(description)
    if key is None:
        return None
