from __future__ import annotations

from dataclasses import dataclass

from pyrl.engine.types.glyphs import Glyph

@dataclass(eq=False, frozen=True)
class Tile:
    """Permanent portion of a square. E.g. walls or floor."""
    name: str
    visible_glyph: Glyph
    memory_glyph: Glyph
    is_passable: bool = True
    is_see_through: bool = True
    move_multi: int = 1
