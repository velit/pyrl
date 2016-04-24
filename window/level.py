from __future__ import absolute_import, division, print_function, unicode_literals

from enums.colors import Pair
from generic_algorithms import bresenham
from window.base_window import BaseWindow


class LevelWindow(BaseWindow):

    """Handles the level display."""

    def update(self):
        self.blit()

    def draw_char(self, char, coord, reverse=False):
        if reverse:
            symbol, (fg, bg) = char
            char = symbol, (bg, fg)
        super().draw_char(char, coord)

    def draw_line(self, coordA, coordB, char=('*', Pair.Yellow), includeFirst=False):
        if includeFirst:
            for coord in bresenham(coordA, coordB):
                self.draw_char(coord, char)
        else:
            for coord in bresenham(coordA, coordB):
                if coord != coordA:
                    self.draw_char(coord, char)
