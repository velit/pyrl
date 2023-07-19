from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field, asdict
from enum import StrEnum
from typing import Any

from pyrl.engine.creature.stats import Stats, Stat
from pyrl.engine.structures.dice import Dice
from pyrl.engine.types.glyphs import Colors, Glyph

class Slot(StrEnum):
    Head       = "Head"
    Body       = "Body"
    Right_Hand = "Right Hand"
    Left_Hand  = "Left Hand"
    Feet       = "Feet"

@dataclass(eq=False)
class Item:
    name: str
    glyph: Glyph
    stats: Stats                       = field(repr=False)
    compatible_slots: tuple[Slot, ...] = field(repr=False)
    uses_all_slots: bool               = False
    damage_dice: Dice | None           = None

    def fits_slot(self, slot: Slot) -> bool:
        return slot in self.compatible_slots

    def weapon_str(self) -> str:
        if self.damage_dice is not None:
            return f" ({self.stats[Stat.ACC]:+}, {self.damage_dice})"
        elif self.stats[Stat.ACC]:
            return f" ({self.stats[Stat.ACC]:+})"
        else:
            return ""

    def armor_str(self) -> str:
        if self.stats[Stat.DEF] or self.stats[Stat.ARMOR]:
            return f" [{self.stats[Stat.DEF]:+}, {self.stats[Stat.ARMOR]:+}]"
        else:
            return ""

    def stats_str(self) -> str:
        skip_stats = Stat.ACC, Stat.DEF, Stat.ARMOR
        stats = ", ".join(f"{stat.short_name}:{value:+}" for stat, value in self.stats.items()
                          if value and stat not in skip_stats)
        if stats:
            return f" {stats}"
        else:
            return ""

    def __str__(self) -> str:
        return f"{self.name}{self.weapon_str()}{self.armor_str()}{self.stats_str()}"

    def __lt__(self, other: Any) -> bool:
        return str(self) < str(other)

# noinspection PyPep8Naming
def Weapon(name: str,
           accuracy: int,
           damage_dice: Dice,
           two_handed: bool = False,
           compatible_slots: Iterable[Slot] = (Slot.Right_Hand, Slot.Left_Hand),
           stats: Stats | None = None,
           glyph: Glyph = ('(', Colors.Normal)) -> Item:
    if stats is None:
        stats = Stats()
    stats[Stat.ACC] = accuracy
    return Item(name=name, glyph=glyph, stats=stats, compatible_slots=tuple(compatible_slots),
                uses_all_slots=two_handed, damage_dice=damage_dice)

# noinspection PyPep8Naming
def Armor(name: str,
          defense: int,
          armor: int,
          compatible_slots: Iterable[Slot] = (),
          stats: Stats | None = None,
          glyph: Glyph = (']', Colors.Normal)) -> Item:
    if stats is None:
        stats = Stats()
    stats[Stat.DEF] = defense
    stats[Stat.ARMOR] = armor
    return Item(name=name, glyph=glyph, stats=stats, compatible_slots=tuple(compatible_slots))
