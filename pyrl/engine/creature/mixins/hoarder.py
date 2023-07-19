from __future__ import annotations

from dataclasses import dataclass, field

from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.inventory import Inventory
from pyrl.engine.creature.stats import Stat
from pyrl.engine.structures.dice import Dice

@dataclass(eq=False)
class Hoarder(Creature):
    """Creatures with this class have an inventory."""

    inventory: Inventory = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.inventory = Inventory(self.update_stats)
        self.register_stat_source(self.inventory)
        super().__post_init__()

    @property
    def damage_dice(self) -> Dice:
        dice = self.inventory.damage_dice
        if dice is not None:
            return Dice(dice.dices, dice.faces, dice.addition + self[Stat.DMG])
        else:
            return super().damage_dice
