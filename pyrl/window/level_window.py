from __future__ import annotations

from pyrl.types.char import Glyph
from pyrl.types.color import ColorPairs
from pyrl.algorithms.coord_algorithms import bresenham
from pyrl.types.coord import Coord
from pyrl.window.base_window import BaseWindow

class LevelWindow(BaseWindow):

    """Handles the level display."""

    def update(self) -> None:
        self.blit()

    def draw_char(self, char: Glyph, coord: Coord, reverse: bool = False) -> None:
        if reverse:
            symbol, (fg, bg) = char
            char = symbol, (bg, fg)
        super().draw_char(char, coord)

    def draw_line(self, a: Coord, b: Coord, char: Glyph = ('*', ColorPairs.Yellow), draw_first: bool = False) -> None:
        if draw_first:
            for coord in bresenham(a, b):
                self.draw_char(char, coord)
        else:
            for coord in bresenham(a, b):
                if coord != a:
                    self.draw_char(char, coord)
