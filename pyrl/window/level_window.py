from __future__ import annotations

from pyrl.constants.colors import ColorPair
from pyrl.generic_algorithms import bresenham
from pyrl.window.base_window import BaseWindow

class LevelWindow(BaseWindow):

    """Handles the level display."""

    def update(self):
        self.blit()

    def draw_char(self, char, coord, reverse=False):
        if reverse:
            symbol, (fg, bg) = char
            char = symbol, (bg, fg)
        super().draw_char(char, coord)

    def draw_line(self, coord_a, coord_b, char=('*', ColorPair.Yellow), include_first=False):
        if include_first:
            for coord in bresenham(coord_a, coord_b):
                self.draw_char(coord, char)
        else:
            for coord in bresenham(coord_a, coord_b):
                if coord != coord_a:
                    self.draw_char(coord, char)
