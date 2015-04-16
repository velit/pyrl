from __future__ import absolute_import, division, print_function, unicode_literals

from enums.colors import Pair
from generic_algorithms import bresenham
from window.base_window import BaseWindow


class LevelWindow(BaseWindow):

    """Handles the level display."""

    def __init__(self, *a, **k):
        BaseWindow.__init__(self, *a, **k)

    def update(self):
        self.blit()

    def draw_char(self, coord, char, reverse=False):
        y, x = coord
        if reverse:
            symbol, (fg, bg) = char
            char = symbol, (bg, fg)
        self.addch(y, x, char)

    def draw_line(self, coordA, coordB, char=('*', Pair.Yellow), includeFirst=False):
        if includeFirst:
            for y, x in bresenham(coordA, coordB):
                self.addch(y, x, char)
        else:
            for y, x in bresenham(coordA, coordB):
                if (y, x) != coordA:
                    self.addch(y, x, char)
