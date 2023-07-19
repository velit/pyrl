from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.stats import Stat, Stats, calculate_stats
from pyrl.engine.types.glyphs import Glyph

@dataclass(frozen=True)
class CreatureTemplate:
    name: str
    glyph: Glyph
    creature_level: int
    spawn_weight_class: int = 0

    def create(self) -> BasicCreature:
        return BasicCreature(self)

@dataclass(eq=False)
class BasicCreature(Creature):

    template: CreatureTemplate
    precalced_stats: ClassVar[dict[int, Stats]] = {}

    def __getitem__(self, stat: Stat) -> int:
        if self.creature_level not in self.precalced_stats:
            self.precalced_stats[self.creature_level] = calculate_stats(self.creature_level, [])
        return self.precalced_stats[self.creature_level][stat]

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
        return CreatureTemplate(name, glyph, creature_level).create()
