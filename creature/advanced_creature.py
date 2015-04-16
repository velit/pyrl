from __future__ import absolute_import, division, print_function, unicode_literals

from .stats import Stat
from .creature import Creature
from .equipment import Equipment


def _add_equipment_properties(cls):
    """Add properties to cls that mesh/add inventory stats to normal stats."""
    for stat in Stat:
        prop = _get_equipment_property(stat)
        setattr(cls, stat.name, prop)
    return cls


def _get_equipment_property(stat):

    def get_stat(self):
        return getattr(super(AdvancedCreature, self), stat.name) + self.equipment.stats[stat]
    get_stat.__name__ = stat.name

    return property(get_stat)


@_add_equipment_properties
class AdvancedCreature(Creature):

    def __init__(self, creature_file):
        self.equipment = Equipment()
        self.inventory = []
        self.last_action_energy = 0

        super().__init__(creature_file)

    def get_damage_info(self):
        damage_info = self.equipment.get_damage_info()
        if damage_info is not None:
            dices, sides, addition = damage_info
            addition += self.damage
        else:
            dices = self.unarmed_dices
            sides = self.unarmed_sides
            addition = self.damage
        return dices, sides, addition

    def get_item(self, slot):
        return self.equipment.items[slot]

    def get_item_stats(self, stat):
        return self.equipment.stats[stat]

    def update_energy(self, amount):
        super().update_energy(amount)
        self.last_action_energy = amount

    def update_energy_action(self, action):
        self.last_action_energy = super().update_energy_action(action)

    def is_idle(self):
        return False

    def equip(self, item, slot):
        self.equipment.equip(slot, item)

    def unequip(self, slot):
        item = self.equipment.items[slot]
        self.equipment.unequip(slot)
        return item

    def bag_item(self, item):
        self.inventory.append(item)

    def unbag_item(self, item):
        self.inventory.remove(item)

    def get_inventory_lines(self):
        f = "{1}. {0.name} {0.stats}"
        for i, item in enumerate(self.inventory):
            yield f.format(item, (i + 1) % 10)

    def get_inventory_items(self, slot=None):
        if slot is not None:
            return (item for item in self.inventory if item.fits_to_slot(slot))
        else:
            return self.inventory
