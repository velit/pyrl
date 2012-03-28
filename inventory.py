from main import io

def inventory(game, creature):
	header = "Inventory"
	inventory_lines = list(creature.get_inventory_lines())
	footer = "Select item to unequip, u/d to scroll, z to close, v to see more items"
	key = io.menu("Inventory", inventory_lines, footer)
