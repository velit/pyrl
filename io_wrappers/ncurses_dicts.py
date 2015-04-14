from __future__ import absolute_import, division, print_function, unicode_literals

import curses
from const.colors import Color
from const.keys import Key


ncurses_key_map = {
    curses.ERR:            Key.NO_INPUT,
    curses.KEY_A1:         Key.NUMPAD_7,
    curses.KEY_A3:         Key.NUMPAD_9,
    curses.KEY_B2:         Key.NUMPAD_5,
    curses.KEY_BACKSPACE:  Key.BACKSPACE,
    curses.KEY_C1:         Key.NUMPAD_1,
    curses.KEY_C3:         Key.NUMPAD_3,
    curses.KEY_DC:         Key.DELETE,
    curses.KEY_DOWN:       Key.DOWN,
    curses.KEY_END:        Key.END,
    curses.KEY_F1:         Key.F1,
    curses.KEY_F2:         Key.F2,
    curses.KEY_F3:         Key.F3,
    curses.KEY_F4:         Key.F4,
    curses.KEY_F5:         Key.F5,
    curses.KEY_F6:         Key.F6,
    curses.KEY_F7:         Key.F7,
    curses.KEY_F8:         Key.F8,
    curses.KEY_F9:         Key.F9,
    curses.KEY_F10:        Key.F10,
    curses.KEY_F11:        Key.F11,
    curses.KEY_F12:        Key.F12,
    curses.KEY_FIND:       Key.NUMPAD_7,
    curses.KEY_HOME:       Key.HOME,
    curses.KEY_IC:         Key.INSERT,
    curses.KEY_LEFT:       Key.LEFT,
    curses.KEY_NPAGE:      Key.PAGE_DOWN,
    curses.KEY_PPAGE:      Key.PAGE_UP,
    curses.KEY_RESIZE:     Key.WINDOW_RESIZE,
    curses.KEY_RIGHT:      Key.RIGHT,
    curses.KEY_SELECT:     Key.NUMPAD_1,
    curses.KEY_UP:         Key.UP,
    curses.ascii.CR:       Key.ENTER,
    curses.ascii.ESC:      Key.ESC,
    curses.ascii.SP:       Key.SPACE,
    curses.ascii.TAB:      Key.TAB,
}


class NCurses256ColorDict(dict):

    color_map = {
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

    def __init__(self):
        dict.__init__(self)
        # 0 is hard-coded to be curses.NORMAL in curses
        self.pair_nr = 1

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            fg, bg = key
            curses.init_pair(self.pair_nr, self.color_map[fg], self.color_map[bg])
            color_pair = curses.color_pair(self.pair_nr)
            self[key] = color_pair
            self.pair_nr += 1
            return color_pair


class NCursesColorDict(dict):

    color_map = {
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

    basic_colors = {
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

    def __init__(self):
        dict.__init__(self)
        # 0 is hard-coded to be NORMAL in curses
        self.pair_nr = 1

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            fg, bg = key
            curses.init_pair(self.pair_nr, self.color_map[fg], self.color_map[bg])
            if fg not in self.basic_colors:
                color_pair = curses.color_pair(self.pair_nr) | curses.A_BOLD
            else:
                color_pair = curses.color_pair(self.pair_nr)
            self[key] = color_pair
            self.pair_nr += 1
            return color_pair
