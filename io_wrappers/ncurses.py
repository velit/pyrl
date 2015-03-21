from __future__ import absolute_import, division, print_function, unicode_literals

import curses
import curses.ascii
import locale
import logging

import const.game as GAME
import const.keys as KEY
from config import debug
from io_wrappers.ncurses_dicts import NCurses256ColorDict, NCursesColorDict, ncurses_key_map


def NCursesWrapper(curses_root_window):
    """
    Properly initialize and return the NCursesWrapper class.

    Implementation must be lazily initialized due to limitations of the curses
    library (color specifically).
    """
    curses.curs_set(0)
    curses.nonl()
    return _NCursesWrapper.init_module(curses_root_window)


class _NCursesWrapper(object):

    _root_window = None

    IMPLEMENTATION = GAME.NCURSES

    key_map = ncurses_key_map
    color_map = None

    locale.setlocale(locale.LC_ALL, "")
    encoding = locale.getpreferredencoding()

    @classmethod
    def init_module(cls, curses_root_window):
        """Module needs to be lazily initialized due to curses colors."""
        if curses.COLORS == 256:
            cls.color_map = NCurses256ColorDict()
        else:
            cls.color_map = NCursesColorDict()

        cls._root_window = cls(curses_root_window)
        return cls

    @staticmethod
    def flush():
        curses.doupdate()

    @staticmethod
    def suspend():
        curses.def_prog_mode()
        curses.reset_shell_mode()
        curses.endwin()

    @staticmethod
    def resume():
        curses.reset_prog_mode()

    @classmethod
    def new_window(cls, size):
        rows, columns = size
        # Writing to the last cell of a window raises an exception because
        # the automatic cursor move to the next cell is illegal. The +1 fixes that.
        window = curses.newpad(rows + 1, columns)
        return cls(window)

    def __init__(self, curses_window):
        self.window = curses_window
        self.window.keypad(True)
        self.window.immedok(False)
        self.window.scrollok(False)

    def addch(self, y, x, char):
        symbol, color = char
        self.window.addch(y, x, symbol.encode(self.encoding), self.color_map[color])

    def addstr(self, y, x, string, color=None):
        if color is None:
            self.window.addstr(y, x, string.encode(self.encoding))
        else:
            self.window.addstr(y, x, string.encode(self.encoding), self.color_map[color])

    def draw(self, char_payload_sequence):
        d = self.window.addch
        local_color = self.color_map
        for y, x, (symbol, color) in char_payload_sequence:
            d(y, x, symbol.encode(self.encoding), local_color[color])

    def draw_reverse(self, char_payload_sequence):
        d = self.window.addch
        local_color = self.color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            d(y, x, symbol.encode(self.encoding), local_color[bg, fg])

    def clear(self):
        self.window.erase()

    def blit(self, size, screen_position):
        self._check_root_window_size()
        rows, cols = size
        y, x = screen_position
        self.window.noutrefresh(0, 0, y, x, y + rows - 1, x + cols - 1)

    def get_dimensions(self):
        return self.window.getmaxyx()

    def move(self, y, x):
        self.window.move(y, x)

    def get_cursor_pos(self):
        return self.window.getyx()

    def get_key(self):
        return self._interpret_ch(self._esc_key_handler(self.window.getch()))

    def check_key(self):
        """Non-blocking version of get_key."""
        self.window.nodelay(True)
        ch = self.get_key()
        self.window.nodelay(False)
        if ch != curses.ERR:
            return ch
        else:
            return KEY.NO_INPUT

    def _interpret_ch(self, ch):

        if ch == curses.KEY_RESIZE:
            self._check_root_window_size()
        elif ch in self.key_map:
            ch = self.key_map[ch]
        else:
            ch = curses.ascii.unctrl(ch)
            if '^' in ch:
                ch = ch.lower()

        if debug.show_keycodes and ch != KEY.NO_INPUT:
            logging.debug("User input: {}".format(ch))

        return ch

    def _esc_key_handler(self, ch):
        if ch == curses.ascii.ESC:
            self.window.nodelay(True)
            second_ch = self.window.getch()
            self.window.nodelay(False)
            if second_ch != curses.ERR:
                return curses.ascii.alt(second_ch)
        return ch

    @classmethod
    def _check_root_window_size(cls):
        rows, cols = cls._root_window.get_dimensions()
        while rows < GAME.SCREEN_ROWS or cols < GAME.SCREEN_COLS:
            message = ("Game needs at least a screen size of {}x{} while the "
                       "current size is {}x{}. Please resize the screen or "
                       "press Q to quit.")
            message = message.format(GAME.SCREEN_COLS, GAME.SCREEN_ROWS, cols, rows)
            cls._root_window.addstr(0, 0, message.encode(cls.encoding))
            cls._root_window.window.refresh()

            if cls._root_window.get_key() == "Q":
                cls._root_window.clear()
                message = "Confirm quit by pressing Y."
                cls._root_window.addstr(0, 0, message.encode(cls.encoding))
                cls._root_window.window.refresh()
                if cls._root_window.get_key() == "Y":
                    exit()
            cls._root_window.clear()
            cls._root_window.window.refresh()
            rows, cols = cls._root_window.get_dimensions()
