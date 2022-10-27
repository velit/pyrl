from __future__ import annotations

from dataclasses import dataclass

from pyrl.engine.behaviour.combat import Attackeable
from pyrl.engine.types.glyphs import Glyph

@dataclass(eq=False, frozen=True)
class Tile(Attackeable):
    """Permanent portion of a square. E.g. walls or floor."""
    name: str
    visible_glyph: Glyph
    memory_glyph: Glyph
    is_passable: bool = True
    is_see_through: bool = True
    move_multi: int = 1

    @property
    def defense(self) -> int:
        return 0

    @property
    def armor(self) -> int:
        return 100 if self.is_passable else 40

    def __repr__(self) -> str:
        return f"Tile({self.name}: {self.visible_glyph[0]})"
