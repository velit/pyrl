from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from .items_view import items_view
from config.bindings import Bind
from creature.equipment import Slot


equipment_slots = OrderedDict()
equipment_slots[Bind.Equipment_Slot_Head.key]       = Slot.head
equipment_slots[Bind.Equipment_Slot_Body.key]       = Slot.body
equipment_slots[Bind.Equipment_Slot_Right_Hand.key] = Slot.right_hand
equipment_slots[Bind.Equipment_Slot_Left_Hand.key]  = Slot.left_hand
equipment_slots[Bind.Equipment_Slot_Feet.key]       = Slot.feet


def equipment(io, char_equipment):
    while True:
        header = "Equipment"
        footer = "Press a slot key to (un)equip, {} to view backpack, {} to close"
        footer = footer.format(Bind.View_Inventory.key, Bind.Cancel.key)
        fmt_str = "{0} - {1:11}: {2}"
        lines = (fmt_str.format(key.upper(), slot.value, char_equipment.get_item(slot)) for key, slot in equipment_slots.items())
        key_seq = tuple(equipment_slots.keys()) + Bind.View_Inventory + Bind.Cancel + ('c',)
        key = io.menu(header, lines, footer, key_seq)
        if key in equipment_slots:
            slot = equipment_slots[key]
            if char_equipment.get_item(slot) is None:
                equipped_item = inventory(io, char_equipment, slot)
                if equipped_item is not None:
                    char_equipment.equip(equipped_item, slot)
            else:
                char_equipment.unequip(equipment_slots[key])
        elif key in Bind.View_Inventory:
            inventory(io, char_equipment)
        #elif key == "c":
            #inventory2(io, char_equipment)
        elif key in Bind.Cancel:
            return


def inventory(io, char_equipment, slot=None):
    header = "Inventory"
    footer = "{} to close".format(Bind.Cancel.key)
    fmt_str = "{0} - {1}"
    inventory_slice = OrderedDict(zip(Bind.item_select_keys, char_equipment.get_inventory_items(slot)))
    lines = (fmt_str.format(key.upper(), item) for key, item in inventory_slice.items())
    key_seq = Bind.Cancel
    if slot is not None:
        key_seq += tuple(inventory_slice.keys())
    key = io.menu(header, lines, footer, key_seq)
    if key in inventory_slice.keys():
        return inventory_slice[key]
    elif key in Bind.Cancel:
        return
    else:
        assert False


def inventory2(io, char_equipment, slot=None):
    header = "Inventory"
    footer = "{} to close".format(Bind.Cancel.key)
    items = char_equipment.get_inventory_items(slot)
    item = items_view(items, io.whole_window, header, footer)
    raise Exception(item)
    #key_seq = Bind.Cancel

    #if slot is not None:
        #key_seq += tuple(inventory_slice.keys())
    #key = io.menu(header, lines, footer, key_seq)
    #if key in inventory_slice.keys():
        #return inventory_slice[key]
    #elif key in Bind.Cancel:
        #return
    #else:
        #assert False
