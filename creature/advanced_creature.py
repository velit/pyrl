from collections import defaultdict

from creature import Creature
from creature.equipment import Equipment
from creature.stats import Stat
from dice import Dice


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

    def __init__(self, name, char, speciation_lvl=0, extinction_lvl=0, coord=None,
                 observe_level_change=True):
        self.equipment = Equipment()
        super().__init__(name, char, speciation_lvl, extinction_lvl, coord)

        self.visited_locations = defaultdict(set)
        self.vision = set()

        if observe_level_change:
            self.outdated_vision_coordinates = set()

    def get_damage_info(self):
        damage_info = self.equipment.get_damage_info()
        if damage_info is not None:
            dices, highest_side, addition = damage_info
            addition += self.damage
        else:
            dices = self.unarmed_dices
            highest_side = self.unarmed_sides
            addition = self.damage
        return Dice(dices, highest_side, addition)

    def is_idle(self):
        return False

    def get_visited_locations(self):
        return self.visited_locations[self.level]

    def add_level_change(self, coord):
        self.outdated_vision_coordinates.add(coord)

    def pop_modified_locations(self):
        locations = self.outdated_vision_coordinates
        self.outdated_vision_coordinates = set()
        return locations

    @property
    def vision(self):
        return self._vision

    @vision.setter
    def vision(self, coordinates):
        self.visited_locations[self.level] |= coordinates
        self._vision = coordinates

    @vision.deleter
    def vision(self):
        del self._vision
