import const.keys as KEY
import const.slots as SLOT
from collections import OrderedDict
from main import io

equipment_keys = OrderedDict()
equipment_keys['h'] = SLOT.HEAD
equipment_keys['b'] = SLOT.BODY
equipment_keys['r'] = SLOT.RIGHT_HAND
equipment_keys['f'] = SLOT.FEET


class Bindings(object):
	VIEW_INVENTORY = 'v'


def equipment(game, creature):
	while True:
		header = "Equipment"
		footer = "Select slot to unequip/equip, {} to view backpack, {} to close"
		footer = footer.format(Bindings.VIEW_INVENTORY, KEY.CANCEL)
		fmt_str = "{0} - {1:11}: {2}"
		lines = []
		for key, slot in equipment_keys.viewitems():
			item = creature.slots[slot]
			if item is None:
				item = "-"
			lines.append(fmt_str.format(key, slot, item))

		key = io.menu(header, lines, footer, equipment_keys.viewkeys() | set((Bindings.VIEW_INVENTORY, )) | KEY.GROUP_DEFAULT)
		if key in equipment_keys:
			unequipped_item = creature.unequip(equipment_keys[key])
			creature.bag_item(unequipped_item)
		elif key == Bindings.VIEW_INVENTORY:
			item = inventory(game, creature)
		elif key in KEY.GROUP_DEFAULT:
			return

def inventory(game, creature):
	while True:
		header = "Inventory"
		footer = "u/d to scroll, {} to close"
		footer = footer.format(KEY.CANCEL)
		lines = creature.get_inventory_lines()
		#fmt_str = "{1:11}: {2}"
		#lines = []
		#for item in creature.equipment_keys.viewitems():
			#item = creature.slots[slot]
			#if item is None:
				#item = "-"
			#lines.append(fmt_str.format(key, slot, item))

		key = io.menu(header, lines, footer, equipment_keys.viewkeys() | KEY.GROUP_DEFAULT)
		if key in KEY.GROUP_DEFAULT:
			return
