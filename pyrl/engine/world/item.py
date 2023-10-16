from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from pyrl.engine.creature.enums.slots import Slot
from pyrl.engine.creature.enums.stats import Stat
from pyrl.engine.enums.glyphs import Glyph, Colors
from pyrl.engine.structures.dice import Dice

@dataclass(eq=False)
class Item:
    name: str
    glyph: Glyph
    compatible_slots: tuple[Slot, ...] = field(repr=False)
    stats: ItemStats                   = field(repr=False, default=())
    uses_all_slots: bool               = False
    damage_dice: Dice | None           = None

    def __getitem__(self, stat: Stat) -> int:
        for item_stat, value in self.stats:
            if item_stat == stat:
                return value
        return 0

    def fits_slot(self, slot: Slot) -> bool:
        return slot in self.compatible_slots

    def weapon_str(self) -> str:
        if self.damage_dice is not None:
            return f" ({self[Stat.ACC]:+}, {self.damage_dice})"
        elif self[Stat.ACC]:
            return f" ({self[Stat.ACC]:+})"
        else:
            return ""

    def armor_str(self) -> str:
        if self[Stat.DEF] or self[Stat.ARMOR]:
            return f" [{self[Stat.DEF]:+}, {self[Stat.ARMOR]:+}]"
        else:
            return ""

    def stats_str(self) -> str:
        skip_stats = Stat.ACC, Stat.DEF, Stat.ARMOR
        stats = ", ".join(f"{stat.short_name}:{value:+}" for stat, value in self.stats
                          if value and stat not in skip_stats)
        if stats:
            return f" {{{stats}}}"
        else:
            return ""

    def __str__(self) -> str:
        return f"{self.name}{self.weapon_str()}{self.armor_str()}{self.stats_str()}"

    def __lt__(self, other: Any) -> bool:
        return str(self) < str(other)

def Weapon(name: str,
           accuracy: int,
           damage_dice: Dice,
           two_handed: bool = False,
           compatible_slots: Iterable[Slot] = (Slot.Right_Hand, Slot.Left_Hand),
           stats: dict[Stat, int] | None = None,
           glyph: Glyph = ('(', Colors.Normal)) -> Item:
    if stats is None:
        stats = {}
    item_stats = ((Stat.ACC, accuracy), *stats.items())
    return Item(name=name, glyph=glyph, stats=item_stats, compatible_slots=tuple(compatible_slots),
                uses_all_slots=two_handed, damage_dice=damage_dice)

def Armor(name: str,
          defense: int,
          armor: int,
          compatible_slots: Iterable[Slot] = (),
          stats: dict[Stat, int] | None = None,
          glyph: Glyph = (']', Colors.Normal)) -> Item:
    if stats is None:
        stats = {}
    item_stats = ((Stat.DEF, defense), (Stat.ARMOR, armor), *stats.items())
    return Item(name=name, glyph=glyph, stats=item_stats, compatible_slots=tuple(compatible_slots))

ItemStat = tuple[Stat, int]
ItemStats = tuple[ItemStat, ...]
