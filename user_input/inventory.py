from pyrl import mappings as MAPPING
import const.slots as SLOT
from collections import OrderedDict
from pyrl.main import io
from pyrl.mappings import CANCEL, GROUP_DEFAULT, VIEW_INVENTORY, INVENTORY_KEYS


equipment_slots = OrderedDict()
equipment_slots[MAPPING.EQUIPMENT_SLOT_HEAD] = SLOT.HEAD
equipment_slots[MAPPING.EQUIPMENT_SLOT_BODY] = SLOT.BODY
equipment_slots[MAPPING.EQUIPMENT_SLOT_RIGHT_HAND] = SLOT.RIGHT_HAND
equipment_slots[MAPPING.EQUIPMENT_SLOT_FEET] = SLOT.FEET


def equipment(game, creature):
    while True:
        header = "Equipment"
        footer = "Press a slot key to (un)equip, {} to view backpack, {} to close"
        footer = footer.format(VIEW_INVENTORY, CANCEL)
        fmt_str = "{0} - {1:11}: {2}"
        lines = (fmt_str.format(key.upper(), slot, creature.get_item(slot)) for key, slot in equipment_slots.viewitems())
        key = io.menu(header, lines, footer, equipment_slots.viewkeys() | set((VIEW_INVENTORY, )) | GROUP_DEFAULT)
        if key in equipment_slots:
            slot = equipment_slots[key]
            if creature.get_item(slot) is None:
                equipped_item = inventory(game, creature, slot)
                if equipped_item is not None:
                    creature.unbag_item(equipped_item)
                    creature.equip(equipped_item, slot)
            else:
                unequipped_item = creature.unequip(equipment_slots[key])
                creature.bag_item(unequipped_item)
        elif key == VIEW_INVENTORY:
            inventory(game, creature)
        elif key in GROUP_DEFAULT:
            return

def inventory(game, creature, slot=None):
    header = "Inventory"
    footer = "{} to close".format(CANCEL)
    fmt_str = "{0} - {1}"
    inventory_slice = OrderedDict(zip(INVENTORY_KEYS, creature.get_inventory_items(slot)))
    lines = (fmt_str.format(key.upper(), item) for key, item in inventory_slice.viewitems())
    key_set = GROUP_DEFAULT
    if slot is not None:
        key_set |= set(inventory_slice.viewkeys())
    key = io.menu(header, lines, footer, key_set)
    if key in inventory_slice.viewkeys():
        return inventory_slice[key]
    elif key in GROUP_DEFAULT:
        return
    else:
        assert False
