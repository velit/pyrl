from __future__ import annotations

from dataclasses import dataclass

from pyrl.types.char import Glyph

@dataclass(eq=False, frozen=True, slots=True)
class Tile:
    """Permanent portion of a square. E.g. walls or floor."""
    name: str
    visible_char: Glyph
    memory_char: Glyph
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
        return f"Tile({self.name}: {self.visible_char[0]})"
