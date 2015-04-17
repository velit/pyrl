from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from creature.equipment import Slot
from config.mappings import Mapping

equipment_slots = OrderedDict()
equipment_slots[Mapping.Equipment_Slot_Head]       = Slot.head
equipment_slots[Mapping.Equipment_Slot_Body]       = Slot.body
equipment_slots[Mapping.Equipment_Slot_Right_Hand] = Slot.right_hand
equipment_slots[Mapping.Equipment_Slot_Left_Hand]  = Slot.left_hand
equipment_slots[Mapping.Equipment_Slot_Feet]       = Slot.feet


def equipment(io, char_equipment):
    while True:
        header = "Equipment"
        footer = "Press a slot key to (un)equip, {} to view backpack, {} to close"
        footer = footer.format(Mapping.View_Inventory, Mapping.Cancel)
        fmt_str = "{0} - {1:11}: {2}"
        lines = (fmt_str.format(key.upper(), slot.value, char_equipment.get_item(slot)) for key, slot in equipment_slots.items())
        key = io.menu(header, lines, footer, equipment_slots.keys() | set((Mapping.View_Inventory, )) | Mapping.Group_Default)
        if key in equipment_slots:
            slot = equipment_slots[key]
            if char_equipment.get_item(slot) is None:
                equipped_item = inventory(io, char_equipment, slot)
                if equipped_item is not None:
                    char_equipment.equip(equipped_item, slot)
            else:
                char_equipment.unequip(equipment_slots[key])
        elif key == Mapping.View_Inventory:
            inventory(io, char_equipment)
        elif key in Mapping.Group_Default:
            return


def inventory(io, char_equipment, slot=None):
    header = "Inventory"
    footer = "{} to close".format(Mapping.Cancel)
    fmt_str = "{0} - {1}"
    inventory_slice = OrderedDict(zip(Mapping.Inventory_Keys, char_equipment.get_inventory_items(slot)))
    lines = (fmt_str.format(key.upper(), item) for key, item in inventory_slice.items())
    key_set = Mapping.Group_Default
    if slot is not None:
        key_set |= set(inventory_slice.keys())
    key = io.menu(header, lines, footer, key_set)
    if key in inventory_slice.keys():
        return inventory_slice[key]
    elif key in Mapping.Group_Default:
        return
    else:
        assert False
