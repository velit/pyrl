from __future__ import annotations

from dataclasses import dataclass

from pyrl.types.glyphs import Colors, Glyph
from pyrl.functions.coord_algorithms import bresenham
from pyrl.types.directions import Coord
from pyrl.window.base_window import BaseWindow

@dataclass(eq=False)
class LevelWindow(BaseWindow):
    """Handles the level display."""

    def update(self) -> None:
        self.blit()

    def draw_glyph(self, glyph: Glyph, coord: Coord, reverse: bool = False) -> None:
        if reverse:
            symbol, (fg, bg) = glyph
            glyph = symbol, (bg, fg)
        super().draw_glyph(glyph, coord)

    def draw_line(self, a: Coord, b: Coord, glyph: Glyph = ('*', Colors.Yellow), draw_first: bool = False) -> None:
        if draw_first:
            for coord in bresenham(a, b):
                self.draw_glyph(glyph, coord)
        else:
            for coord in bresenham(a, b):
                if coord != a:
                    self.draw_glyph(glyph, coord)
