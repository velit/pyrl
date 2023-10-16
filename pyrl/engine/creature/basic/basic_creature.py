from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from pyrl.engine.creature.enums.traits import Trait
from pyrl.engine.enums.mods import Mod
from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.enums.stats import Stat, Stats, calculate_stats
from pyrl.engine.enums.glyphs import Glyph

@dataclass(frozen=True)
class BasicCreatureTemplate:
    name:               str
    glyph:              Glyph = field(repr=False)
    creature_level:     int
    spawn_weight_class: int = 0
    traits:             list[Trait] = field(default_factory=list)
    mods:               dict[Stat, Mod] = field(default_factory=dict)

    def create(self) -> BasicCreature:
        return BasicCreature(self)

@dataclass(eq=False)
class BasicCreature(Creature):

    template: BasicCreatureTemplate
    precalced_stats: ClassVar[dict[int, Stats]] = {}

    def __getitem__(self, stat: Stat) -> int:
        if self.creature_level not in self.precalced_stats:
            self.precalced_stats[self.creature_level] = calculate_stats(self.creature_level, [])
        if stat in self.mods:
            return round(self.precalced_stats[self.creature_level][stat] * self.mods[stat].mod)
        return self.precalced_stats[self.creature_level][stat]

    @property
    def mods(self) -> dict[Stat, Mod]:
        return self.template.mods

    @property
    def name(self) -> str:
        return self.template.name

    @property
    def glyph(self) -> Glyph:
        return self.template.glyph

    @property
    def creature_level(self) -> int:
        return self.template.creature_level

    @staticmethod
    def create(name: str, glyph: Glyph, creature_level: int) -> BasicCreature:
        return BasicCreatureTemplate(name, glyph, creature_level).create()
