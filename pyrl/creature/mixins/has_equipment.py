import typing

from pyrl.creature.creature import Creature
from pyrl.creature.equipment import Equipment
from pyrl.creature.stats import Stat
from pyrl.dice import Dice

def _get_equipment_property(stat):

    def get_stat(self):
        return getattr(super(HasEquipment, self), stat.name) + self.equipment.applied_stats[stat]
    get_stat.__name__ = stat.name

    return property(get_stat)

def _add_equipment_properties(cls):
    """Add equipment properties to cls that modify normal stats."""
    for stat in Stat:
        prop = _get_equipment_property(stat)
        setattr(cls, stat.name, prop)
    return cls

if typing.TYPE_CHECKING:
    CreatureHint = Creature
else:
    CreatureHint = object

@_add_equipment_properties
class HasEquipment(CreatureHint):

    """Creatures with this mixin class have an equipment and a bag."""

    def __init__(self, *args, **kwargs):
        self.equipment = Equipment()
        super().__init__(*args, **kwargs)

    def get_damage_info(self) -> Dice:
        info = self.equipment.get_damage_info()
        if info is not None:
            return Dice(info.dices, info.faces, info.addition + self.damage)
        else:
            return super().get_damage_info()
