from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from .lines_view import lines_view
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
        footer = "Press a slot key to (un)equip  {} to view backpack  {} to close"
        footer = footer.format(Bind.View_Inventory.key, Bind.Cancel.key)
        fmt_str = "{0} - {1:11}: {2}"
        lines = (fmt_str.format(key.upper(), slot.value, char_equipment.get_item(slot)) for key, slot in equipment_slots.items())
        key_seq = tuple(equipment_slots.keys()) + Bind.View_Inventory + Bind.Cancel + ('c',)
        key = io.menu(header, lines, footer, key_seq)

        if key in Bind.Cancel:
            return
        elif key in Bind.View_Inventory:
            inventory(io, char_equipment)
        elif key in equipment_slots:
            slot = equipment_slots[key]
            if char_equipment.get_item(slot) is None:
                equipped_item = inventory(io, char_equipment, slot)
                if equipped_item is not None:
                    char_equipment.equip(equipped_item, slot)
            else:
                char_equipment.unequip(equipment_slots[key])


def inventory(io, char_equipment, slot=None):
    if slot is None:
        header = "Inventory"
        use_selectable_items = False
    else:
        header = "Select item to equip"
        use_selectable_items = True

    items = char_equipment.get_inventory_items(slot)
    lines = tuple(str(item) for item in items)
    index = lines_view(io.whole_window, lines, header, use_selectable_items)
    if index is not None:
        return items[index]
