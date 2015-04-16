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
        return getattr(super(AdvancedCreature, self), stat.name) + self.equipment.applied_stats[stat]
    get_stat.__name__ = stat.name

    return property(get_stat)


@_add_equipment_properties
class AdvancedCreature(Creature):

    def __init__(self, creature_file):
        self.equipment = Equipment()
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

    def update_energy(self, amount):
        super().update_energy(amount)
        self.last_action_energy = amount

    def update_energy_action(self, action):
        self.last_action_energy = super().update_energy_action(action)

    def is_idle(self):
        return False
