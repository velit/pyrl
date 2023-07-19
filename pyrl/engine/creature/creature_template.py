from __future__ import annotations

from dataclasses import dataclass

from pyrl.engine.creature.creature import Creature
from pyrl.engine.types.glyphs import Glyph

@dataclass(frozen=True)
class CreatureTemplate:
    name: str
    glyph: Glyph
    creature_level: int
    spawn_weight_class: int

    def create(self) -> Creature:
        return Creature(self.name, self.glyph, self.creature_level)
