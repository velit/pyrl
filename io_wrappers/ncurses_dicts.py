from __future__ import absolute_import, division, print_function, unicode_literals

import curses
import const.colors as COLOR
import const.keys as KEY


ncurses_key_map = {
    curses.ERR:            KEY.NO_INPUT,
    curses.KEY_A1:         KEY.NUMPAD_7,
    curses.KEY_A3:         KEY.NUMPAD_9,
    curses.KEY_B2:         KEY.NUMPAD_5,
    curses.KEY_BACKSPACE:  KEY.BACKSPACE,
    curses.KEY_C1:         KEY.NUMPAD_1,
    curses.KEY_C3:         KEY.NUMPAD_3,
    curses.KEY_DC:         KEY.DELETE,
    curses.KEY_DOWN:       KEY.DOWN,
    curses.KEY_END:        KEY.END,
    curses.KEY_F1:         KEY.F1,
    curses.KEY_F2:         KEY.F2,
    curses.KEY_F3:         KEY.F3,
    curses.KEY_F4:         KEY.F4,
    curses.KEY_F5:         KEY.F5,
    curses.KEY_F6:         KEY.F6,
    curses.KEY_F7:         KEY.F7,
    curses.KEY_F8:         KEY.F8,
    curses.KEY_F9:         KEY.F9,
    curses.KEY_F10:        KEY.F10,
    curses.KEY_F11:        KEY.F11,
    curses.KEY_F12:        KEY.F12,
    curses.KEY_FIND:       KEY.NUMPAD_7,
    curses.KEY_HOME:       KEY.HOME,
    curses.KEY_IC:         KEY.INSERT,
    curses.KEY_LEFT:       KEY.LEFT,
    curses.KEY_NPAGE:      KEY.PAGE_DOWN,
    curses.KEY_PPAGE:      KEY.PAGE_UP,
    curses.KEY_RESIZE:     KEY.WINDOW_RESIZE,
    curses.KEY_RIGHT:      KEY.RIGHT,
    curses.KEY_SELECT:     KEY.NUMPAD_1,
    curses.KEY_UP:         KEY.UP,
    curses.ascii.CR:       KEY.ENTER,
    curses.ascii.ESC:      KEY.ESC,
    curses.ascii.SP:       KEY.SPACE,
    curses.ascii.TAB:      KEY.TAB,
}


class NCurses256ColorDict(dict):

    CURSES_ATTR = {

        COLOR.BASE_RED:           124,
        COLOR.BASE_GREEN:         34,
        COLOR.BASE_BLUE:          21,
        COLOR.BASE_PURPLE:        129,
        COLOR.BASE_CYAN:          37,
        COLOR.BASE_YELLOW:        227,
        COLOR.BASE_BROWN:         130,
        COLOR.BASE_DARK_BLUE:     19,
        COLOR.BASE_DARK_BROWN:    94,
        COLOR.BASE_LIGHT_RED:     203,
        COLOR.BASE_LIGHT_GREEN:   83,
        COLOR.BASE_LIGHT_BLUE:    63,
        COLOR.BASE_LIGHT_PURPLE:  207,
        COLOR.BASE_LIGHT_CYAN:    87,
        COLOR.BASE_WHITE:         231,
        COLOR.BASE_LIGHT:         253,
        COLOR.BASE_NORMAL:        7,
        COLOR.BASE_LIGHT_GRAY:    248,
        COLOR.BASE_GRAY:          245,
        COLOR.BASE_DARK_GRAY:     242,
        COLOR.BASE_DARK:          239,
        COLOR.BASE_DARKER:        236,
        COLOR.BASE_DARKEST:       233,
        COLOR.BASE_BLACK:         16,
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
            curses.init_pair(self.pair_nr, self.CURSES_ATTR[fg], self.CURSES_ATTR[bg])
            color_pair = curses.color_pair(self.pair_nr)
            self[key] = color_pair
            self.pair_nr += 1
            return color_pair


class NCursesColorDict(dict):

    C = COLOR
    CURSES_ATTR = {
        C.BASE_RED:           curses.COLOR_RED,
        C.BASE_GREEN:         curses.COLOR_GREEN,
        C.BASE_BLUE:          curses.COLOR_BLUE,
        C.BASE_PURPLE:        curses.COLOR_MAGENTA,
        C.BASE_CYAN:          curses.COLOR_CYAN,
        C.BASE_YELLOW:        curses.COLOR_YELLOW,
        C.BASE_BROWN:         curses.COLOR_YELLOW,
        C.BASE_DARK_BLUE:     curses.COLOR_BLUE,
        C.BASE_DARK_BROWN:    curses.COLOR_YELLOW,
        C.BASE_LIGHT_RED:     curses.COLOR_RED,
        C.BASE_LIGHT_GREEN:   curses.COLOR_GREEN,
        C.BASE_LIGHT_BLUE:    curses.COLOR_BLUE,
        C.BASE_LIGHT_PURPLE:  curses.COLOR_MAGENTA,
        C.BASE_LIGHT_CYAN:    curses.COLOR_CYAN,
        C.BASE_WHITE:         curses.COLOR_WHITE,
        C.BASE_LIGHT:         curses.COLOR_WHITE,
        C.BASE_NORMAL:        curses.COLOR_WHITE,
        C.BASE_LIGHT_GRAY:    curses.COLOR_WHITE,
        C.BASE_GRAY:          curses.COLOR_WHITE,
        C.BASE_DARK_GRAY:     curses.COLOR_WHITE,
        C.BASE_DARK:          curses.COLOR_BLACK,
        C.BASE_DARKER:        curses.COLOR_BLACK,
        C.BASE_DARKEST:       curses.COLOR_BLACK,
        C.BASE_BLACK:         curses.COLOR_BLACK,
    }

    BASIC_COLORS = {
        C.BASE_NORMAL,
        C.BASE_WHITE,
        C.BASE_BLACK,
        C.BASE_RED,
        C.BASE_GREEN,
        C.BASE_BLUE,
        C.BASE_PURPLE,
        C.BASE_CYAN,
        C.BASE_BROWN,
        C.BASE_DARK_GRAY,
        C.BASE_GRAY,
        C.BASE_LIGHT_GRAY,
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
            curses.init_pair(self.pair_nr, self.CURSES_ATTR[fg], self.CURSES_ATTR[bg])
            if fg not in self.BASIC_COLORS:
                color_pair = curses.color_pair(self.pair_nr) | curses.A_BOLD
            else:
                color_pair = curses.color_pair(self.pair_nr)
            self[key] = color_pair
            self.pair_nr += 1
            return color_pair
