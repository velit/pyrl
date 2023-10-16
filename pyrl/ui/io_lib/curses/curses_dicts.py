from __future__ import annotations

import curses
import sys

assert sys.platform != "win32"

from pyrl.engine.enums.glyphs import Color, ColorPair

class Curses256ColorDict(dict[ColorPair, int]):

    color_map: dict[Color, int] = {
        Color.Red:           124,
        Color.Green:         34,
        Color.Blue:          21,
        Color.Purple:        129,
        Color.Cyan:          37,
        Color.Yellow:        227,
        Color.Brown:         130,
        Color.Dark_Blue:     19,
        Color.Dark_Brown:    94,
        Color.Light_Red:     203,
        Color.Light_Green:   83,
        Color.Light_Blue:    63,
        Color.Light_Purple:  207,
        Color.Light_Cyan:    87,
        Color.White:         231,
        Color.Light:         253,
        Color.Normal:        7,
        Color.Light_Gray:    248,
        Color.Gray:          245,
        Color.Dark_Gray:     242,
        Color.Dark:          239,
        Color.Darker:        236,
        Color.Darkest:       233,
        Color.Black:         16,
    }

    def __init__(self) -> None:
        super().__init__(self)
        # 0 is hard-coded to be curses.NORMAL in curses
        self.pair_nr = 1

    def __getitem__(self, color_pair: ColorPair) -> int:
        try:
            return super().__getitem__(color_pair)
        except KeyError:
            fg, bg = color_pair
            curses.init_pair(self.pair_nr, self.color_map[fg], self.color_map[bg])
            curses_color_pair = curses.color_pair(self.pair_nr)
            self[color_pair] = curses_color_pair
            self.pair_nr += 1
            return curses_color_pair

class CursesColorDict(dict[ColorPair, int]):

    color_map: dict[Color, int] = {
        Color.Red:           curses.COLOR_RED,
        Color.Green:         curses.COLOR_GREEN,
        Color.Blue:          curses.COLOR_BLUE,
        Color.Purple:        curses.COLOR_MAGENTA,
        Color.Cyan:          curses.COLOR_CYAN,
        Color.Yellow:        curses.COLOR_YELLOW,
        Color.Brown:         curses.COLOR_YELLOW,
        Color.Dark_Blue:     curses.COLOR_BLUE,
        Color.Dark_Brown:    curses.COLOR_YELLOW,
        Color.Light_Red:     curses.COLOR_RED,
        Color.Light_Green:   curses.COLOR_GREEN,
        Color.Light_Blue:    curses.COLOR_BLUE,
        Color.Light_Purple:  curses.COLOR_MAGENTA,
        Color.Light_Cyan:    curses.COLOR_CYAN,
        Color.White:         curses.COLOR_WHITE,
        Color.Light:         curses.COLOR_WHITE,
        Color.Normal:        curses.COLOR_WHITE,
        Color.Light_Gray:    curses.COLOR_WHITE,
        Color.Gray:          curses.COLOR_WHITE,
        Color.Dark_Gray:     curses.COLOR_WHITE,
        Color.Dark:          curses.COLOR_BLACK,
        Color.Darker:        curses.COLOR_BLACK,
        Color.Darkest:       curses.COLOR_BLACK,
        Color.Black:         curses.COLOR_BLACK,
    }

    basic_colors: set[Color] = {
        Color.Normal,
        Color.White,
        Color.Black,
        Color.Red,
        Color.Green,
        Color.Blue,
        Color.Purple,
        Color.Cyan,
        Color.Brown,
        Color.Dark_Gray,
        Color.Gray,
        Color.Light_Gray,
    }

    def __init__(self) -> None:
        super().__init__(self)
        # 0 is hard-coded to be NORMAL in curses
        self.pair_nr = 1

    def __getitem__(self, color_pair: ColorPair) -> int:
        try:
            return super().__getitem__(color_pair)
        except KeyError:
            fg, bg = color_pair
            curses.init_pair(self.pair_nr, self.color_map[fg], self.color_map[bg])
            if fg not in self.basic_colors:
                curses_color_pair = curses.color_pair(self.pair_nr) | curses.A_BOLD
            else:
                curses_color_pair = curses.color_pair(self.pair_nr)
            self[color_pair] = curses_color_pair
            self.pair_nr += 1
            return curses_color_pair
