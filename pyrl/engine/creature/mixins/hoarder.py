from __future__ import annotations

from dataclasses import dataclass, field

from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.inventory import Inventory
from pyrl.engine.structures.dice import Dice

@dataclass(eq=False)
class Hoarder(Creature):
    """Creatures with this class have an inventory."""

    inventory: Inventory = field(init=False, repr=False, default_factory=Inventory)

    @property
    def damage_dice(self) -> Dice:
        dice = self.inventory.damage_dice
        if dice is not None:
            return Dice(dice.dices, dice.faces, dice.addition + self.damage)
        else:
            return super().damage_dice

    @property
    def strength(self) -> int:
        return super().strength + self.inventory.stats.strength

    @property
    def dexterity(self) -> int:
        return super().dexterity + self.inventory.stats.dexterity

    @property
    def intelligence(self) -> int:
        return super().intelligence + self.inventory.stats.intelligence

    @property
    def endurance(self) -> int:
        return super().endurance + self.inventory.stats.endurance

    @property
    def perception(self) -> int:
        return super().perception + self.inventory.stats.perception

    @property
    def accuracy(self) -> int:
        return super().accuracy + self.inventory.stats.accuracy

    @property
    def armor(self) -> int:
        return super().armor + self.inventory.stats.armor

    @property
    def damage(self) -> int:
        return super().damage + self.inventory.stats.damage

    @property
    def defense(self) -> int:
        return super().defense + self.inventory.stats.defense

    @property
    def max_hp(self) -> int:
        return super().max_hp + self.inventory.stats.max_hp

    @property
    def sight(self) -> int:
        return super().sight + self.inventory.stats.sight

    @property
    def speed(self) -> int:
        return super().speed + self.inventory.stats.speed
