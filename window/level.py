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
        if reverse:
            char = char[0], char[1][1], char[1][0]
        super().draw_char(coord, char)

    def draw_line(self, coordA, coordB, char=('*', Pair.Yellow), includeFirst=False):
        if includeFirst:
            for coord in bresenham(coordA, coordB):
                self.draw_char(coord, char)
        else:
            for coord in bresenham(coordA, coordB):
                if coord != coordA:
                    self.draw_char(coord, char)
