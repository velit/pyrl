from window.base_window import BaseWindow
from pyrl.generic_algorithms import bresenham
from const.colors import YELLOW


class LevelWindow(BaseWindow):
    """Handles the level display"""

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

    def draw_line(self, coordA, coordB, char=('*', YELLOW), includeFirst=False):
        if includeFirst:
            for y, x in bresenham(coordA, coordB):
                self.addch(y, x, char)
        else:
            for y, x in bresenham(coordA, coordB):
                if (y, x) != coordA:
                    self.addch(y, x, char)
