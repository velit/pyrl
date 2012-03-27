from main import io

def inventory(game, creature):
	inventory_lines = list(creature.get_inventory_lines())
	key = io.menu("Inventory", inventory_lines)
