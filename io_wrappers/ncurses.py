from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import curses
import curses.ascii
import locale

import const.colors as COLOR
import const.game as GAME
import const.keys as KEY
from config import debug


class Curses256ColorDict(dict):

    CURSES_ATTR = {

        COLOR.BASE_RED: 124,           COLOR.BASE_GREEN: 34,
        COLOR.BASE_BLUE: 21,

        COLOR.BASE_PURPLE: 129,        COLOR.BASE_CYAN: 37,
        COLOR.BASE_YELLOW: 227,        COLOR.BASE_BROWN: 130,

        COLOR.BASE_DARK_BLUE: 19,      COLOR.BASE_DARK_BROWN: 94,

        COLOR.BASE_LIGHT_RED: 203,     COLOR.BASE_LIGHT_GREEN: 83,
        COLOR.BASE_LIGHT_BLUE: 63,

        COLOR.BASE_LIGHT_PURPLE: 207,  COLOR.BASE_LIGHT_CYAN: 87,

        COLOR.BASE_WHITE: 231,         COLOR.BASE_LIGHT: 253,
        COLOR.BASE_NORMAL: 7,          COLOR.BASE_LIGHT_GRAY: 248,
        COLOR.BASE_GRAY: 245,          COLOR.BASE_DARK_GRAY: 242,
        COLOR.BASE_DARK: 239,          COLOR.BASE_DARKER: 236,
        COLOR.BASE_DARKEST: 233,       COLOR.BASE_BLACK: 16,
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


class CursesColorDict(dict):

    C = COLOR
    CURSES_ATTR = {
        C.BASE_RED: curses.COLOR_RED,               C.BASE_GREEN: curses.COLOR_GREEN,
        C.BASE_BLUE: curses.COLOR_BLUE,

        C.BASE_PURPLE: curses.COLOR_MAGENTA,        C.BASE_CYAN: curses.COLOR_CYAN,
        C.BASE_YELLOW: curses.COLOR_YELLOW,         C.BASE_BROWN: curses.COLOR_YELLOW,

        C.BASE_DARK_BLUE: curses.COLOR_BLUE,        C.BASE_DARK_BROWN: curses.COLOR_YELLOW,

        C.BASE_LIGHT_RED: curses.COLOR_RED,         C.BASE_LIGHT_GREEN: curses.COLOR_GREEN,
        C.BASE_LIGHT_BLUE: curses.COLOR_BLUE,

        C.BASE_LIGHT_PURPLE: curses.COLOR_MAGENTA,  C.BASE_LIGHT_CYAN: curses.COLOR_CYAN,

        C.BASE_WHITE: curses.COLOR_WHITE,           C.BASE_LIGHT: curses.COLOR_WHITE,
        C.BASE_NORMAL: curses.COLOR_WHITE,          C.BASE_LIGHT_GRAY: curses.COLOR_WHITE,
        C.BASE_GRAY: curses.COLOR_WHITE,            C.BASE_DARK_GRAY: curses.COLOR_WHITE,
        C.BASE_DARK: curses.COLOR_BLACK,            C.BASE_DARKER: curses.COLOR_BLACK,
        C.BASE_DARKEST: curses.COLOR_BLACK,         C.BASE_BLACK: curses.COLOR_BLACK,
    }

    BASIC_COLORS = {
        C.BASE_NORMAL,  C.BASE_WHITE,
        C.BASE_BLACK,   C.BASE_RED,
        C.BASE_GREEN,   C.BASE_BLUE,
        C.BASE_PURPLE,  C.BASE_CYAN,
        C.BASE_BROWN,   C.BASE_DARK_GRAY,
        C.BASE_GRAY,    C.BASE_LIGHT_GRAY,
    }

    def __init__(self):
        dict.__init__(self)
        # 0 is hard-coded to be NORMAL
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


class NCursesWrapper(object):

    def __init__(self, root_window):
        self.root_window = root_window

        curses.curs_set(0)
        curses.nonl()

        if curses.COLORS == 256:
            self.color_map = Curses256ColorDict()
        else:
            self.color_map = CursesColorDict()
        self._window_resized()

        locale.setlocale(locale.LC_ALL, "")
        self.encoding = locale.getpreferredencoding()

        c = curses
        self.key_map = {
            c.ERR: KEY.NO_INPUT,         c.KEY_A1: KEY.NUMPAD_7,           c.KEY_A3: KEY.NUMPAD_9,
            c.KEY_B2: KEY.NUMPAD_5,      c.KEY_BACKSPACE: KEY.BACKSPACE,   c.KEY_C1: KEY.NUMPAD_1,
            c.KEY_C3: KEY.NUMPAD_3,      c.KEY_DC: KEY.DELETE,             c.KEY_DOWN: KEY.DOWN,
            c.KEY_END: KEY.END,          c.KEY_F1: KEY.F1,                 c.KEY_F2: KEY.F2,
            c.KEY_F3: KEY.F3,            c.KEY_F4: KEY.F4,                 c.KEY_F5: KEY.F5,
            c.KEY_F6: KEY.F6,            c.KEY_F7: KEY.F7,                 c.KEY_F8: KEY.F8,
            c.KEY_F9: KEY.F9,            c.KEY_F10: KEY.F10,               c.KEY_F11: KEY.F11,
            c.KEY_F12: KEY.F12,          c.KEY_FIND: KEY.NUMPAD_7,         c.KEY_HOME: KEY.HOME,
            c.KEY_IC: KEY.INSERT,        c.KEY_LEFT: KEY.LEFT,             c.KEY_NPAGE: KEY.PAGE_DOWN,
            c.KEY_PPAGE: KEY.PAGE_UP,    c.KEY_RESIZE: KEY.WINDOW_RESIZE,  c.KEY_RIGHT: KEY.RIGHT,
            c.KEY_SELECT: KEY.NUMPAD_1,  c.KEY_UP: KEY.UP,                 c.ascii.CR: KEY.ENTER,
            c.ascii.ESC: KEY.ESC,        c.ascii.SP: KEY.SPACE,            c.ascii.TAB: KEY.TAB,
        }

    def init_handle(self, window):
        window.keypad(True)
        window.immedok(False)
        window.scrollok(False)

    def new_window(self, size):
        rows, columns = size

        # Writing to the last cell of a window raises an exception because
        # the automatic cursor move to the next cell is illegal. The +1 fixes that.
        window = curses.newpad(rows + 1, columns)

        self.init_handle(window)
        return window

    def _window_resized(self):
        rows, cols = self.get_dimensions(self.root_window)
        while rows < GAME.SCREEN_ROWS or cols < GAME.SCREEN_COLS:
            message = "Game needs at least a screen size of {}x{} while the current size is {}x{}. " \
                "Please resize the screen or press Q to quit immediately."
            self.addstr(self.root_window, 0, 0, message.format(GAME.SCREEN_COLS, GAME.SCREEN_ROWS, cols, rows))
            if self.root_window.getch() == "Q":
                exit()
            rows, cols = self.get_dimensions(self.root_window)
            self.root_window.erase()
            self.root_window.refresh()

    def flush(self):
        curses.doupdate()

    def get_root_window(self):
        return self.root_window

    def suspend(self):
        curses.def_prog_mode()
        curses.reset_shell_mode()
        curses.endwin()

    def resume(self):
        curses.reset_prog_mode()

    def addch(self, window, y, x, char):
        symbol, color = char
        window.addch(y, x, symbol.encode(self.encoding), self.color_map[color])

    def addstr(self, window, y, x, string, color=None):
        if color is None:
            window.addstr(y, x, string.encode(self.encoding))
        else:
            window.addstr(y, x, string.encode(self.encoding), self.color_map[color])

    def draw(self, window, char_payload_sequence):
        f = window.addch
        COLOR_LOOKUP = self.color_map
        for y, x, (symbol, color) in char_payload_sequence:
            f(y, x, symbol.encode(self.encoding), COLOR_LOOKUP[color])

    def draw_reverse(self, window, char_payload_sequence):
        f = window.addch
        COLOR_LOOKUP = self.color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            f(y, x, symbol.encode(self.encoding), COLOR_LOOKUP[bg, fg])

    def _esc_key_handler(self, window, ch):
        if ch == curses.ascii.ESC:
            window.nodelay(True)
            second_ch = window.getch()
            window.nodelay(False)
            if second_ch != curses.ERR:
                return curses.ascii.alt(second_ch)
        return ch

    def _interpret_ch(self, ch):

        if ch == curses.KEY_RESIZE:
            self._window_resized()
        elif ch in self.key_map:
            ch = self.key_map[ch]
        else:
            ch = curses.ascii.unctrl(ch)
            if '^' in ch:
                ch = ch.lower()

        if debug.show_keycodes and ch != KEY.NO_INPUT:
            logging.debug("User input: {}".format(ch))

        return ch

    def get_key(self, window):
        return self._interpret_ch(self._esc_key_handler(window, window.getch()))

    def check_key(self, window):
        """Non-blocking version of get_key."""
        window.nodelay(True)
        ch = self.get_key(window)
        window.nodelay(False)
        if ch != curses.ERR:
            return ch
        else:
            return KEY.NO_INPUT

    def clear(self, window):
        window.erase()

    def blit(self, window, size, screen_position):
        screen_rows, screen_cols = self.get_dimensions(self.root_window)
        if screen_rows < GAME.SCREEN_ROWS or screen_cols < GAME.SCREEN_COLS:
            self._window_resized()
        rows, cols = size
        y, x = screen_position
        window.noutrefresh(0, 0, y, x, y + rows - 1, x + cols - 1)

    def get_dimensions(self, window):
        rows, columns = window.getmaxyx()
        return rows, columns

    def move(self, window, y, x):
        window.move(y, x)

    def get_cursor_pos(self, window):
        return window.getyx()

    def get_implementation(self):
        return GAME.NCURSES
