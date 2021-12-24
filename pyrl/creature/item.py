from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field, asdict
from typing import Any

from pyrl.creature.stats import Stats, Stat
from pyrl.dice import Dice
from pyrl.constants.colors import ColorPair
from pyrl.constants.char import Char
from pyrl.constants.equipment_slot import Slot

@dataclass(eq=False, slots=True)
class Item:
    name: str
    char: Char
    stats: Stats                       = field(repr=False)
    compatible_slots: tuple[Slot, ...] = field(repr=False)
    uses_all_slots: bool               = False
    damage_dice: Dice | None           = None

    def fits_slot(self, slot: Slot) -> bool:
        return slot in self.compatible_slots

    def weapon_str(self) -> str:
        if self.damage_dice is not None:
            return f" ({self.stats.accuracy:+}, {self.damage_dice})"
        elif self.stats.accuracy:
            return f" ({self.stats.accuracy:+})"
        else:
            return ""

    def armor_str(self) -> str:
        if self.stats.defense or self.stats.armor:
            return f" [{self.stats.defense:+}, {self.stats.armor:+}]"
        else:
            return ""

    def stats_str(self) -> str:
        skip_stats = ("weapon_dice", "accuracy", "defense", "armor")
        stats_dict: dict[str, int] = asdict(self.stats)
        stat: str
        value: int
        stats = ", ".join(f"{Stat[stat].value}:{value:+}"
                          for stat, value in stats_dict.items()
                          if value and stat not in skip_stats)
        if stats:
            return f" {stats}"
        else:
            return ""

    def __str__(self) -> str:
        return f"{self.name}{self.weapon_str()}{self.armor_str()}{self.stats_str()}"

    def __lt__(self, other: Any) -> bool:
        return str(self) < str(other)

    def __repr__(self) -> str:
        return f"Item({self.name=}, {self.char=}, {self.compatible_slots=}, {self.stats=})"

# noinspection PyPep8Naming
def Weapon(name: str,
           accuracy: int,
           damage_dice: Dice,
           two_handed: bool = False,
           compatible_slots: Iterable[Slot] = (Slot.Right_Hand, Slot.Left_Hand),
           stats: Stats = None,
           char: Char = ('(', ColorPair.Normal)) -> Item:
    if stats is None:
        stats = Stats()
    stats.accuracy = accuracy
    return Item(name=name, char=char, stats=stats, compatible_slots=tuple(compatible_slots),
                uses_all_slots=two_handed, damage_dice=damage_dice)

# noinspection PyPep8Naming
def Armor(name: str,
          defense: int,
          armor: int,
          compatible_slots: Iterable[Slot] = (),
          stats: Stats = None,
          char: Char = (']', ColorPair.Normal)) -> Item:
    if stats is None:
        stats = Stats()
    stats.defense = defense
    stats.armor = armor
    return Item(name=name, char=char, stats=stats, compatible_slots=tuple(compatible_slots))
