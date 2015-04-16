from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from creature.equipment import Slot
from mappings import Mapping

equipment_slots = OrderedDict()
equipment_slots[Mapping.Equipment_Slot_Head]       = Slot.head
equipment_slots[Mapping.Equipment_Slot_Body]       = Slot.body
equipment_slots[Mapping.Equipment_Slot_Right_Hand] = Slot.right_hand
equipment_slots[Mapping.Equipment_Slot_Left_Hand]  = Slot.left_hand
equipment_slots[Mapping.Equipment_Slot_Feet]       = Slot.feet


def equipment(io, game, creature):
    while True:
        header = "Equipment"
        footer = "Press a slot key to (un)equip, {} to view backpack, {} to close"
        footer = footer.format(Mapping.View_Inventory, Mapping.Cancel)
        fmt_str = "{0} - {1:11}: {2}"
        lines = (fmt_str.format(key.upper(), slot.value, creature.get_item(slot)) for key, slot in equipment_slots.items())
        key = io.menu(header, lines, footer, equipment_slots.keys() | set((Mapping.View_Inventory, )) | Mapping.Group_Default)
        if key in equipment_slots:
            slot = equipment_slots[key]
            if creature.get_item(slot) is None:
                equipped_item = inventory(io, game, creature, slot)
                if equipped_item is not None:
                    creature.unbag_item(equipped_item)
                    creature.equip(equipped_item, slot)
            else:
                unequipped_item = creature.unequip(equipment_slots[key])
                creature.bag_item(unequipped_item)
        elif key == Mapping.View_Inventory:
            inventory(io, game, creature)
        elif key in Mapping.Group_Default:
            return


def inventory(io, game, creature, slot=None):
    header = "Inventory"
    footer = "{} to close".format(Mapping.Cancel)
    fmt_str = "{0} - {1}"
    inventory_slice = OrderedDict(zip(Mapping.Inventory_Keys, creature.get_inventory_items(slot)))
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
