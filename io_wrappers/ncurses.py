from __future__ import absolute_import, division, print_function, unicode_literals

import curses
import curses.ascii
import locale
import logging

import const.game as GAME
import const.keys as KEY
from config import debug
from io_wrappers.ncurses_dicts import NCurses256ColorDict, NCursesColorDict, ncurses_key_map


def _init_curses(curses_root_window=None):
    if curses_root_window is None:
        curses_root_window = curses.initscr()
        curses.start_color()
    curses.curs_set(0)
    curses.nonl()
    return curses_root_window


class NCursesWrapper(object):

    IMPLEMENTATION = GAME.NCURSES

    def __init__(self, curses_root_window=None):
        """Initialize curses if not already and initialize NCursesWindow."""
        NCursesWindow.init_class_attributes(_init_curses(curses_root_window))

    def new_window(self, dimensions):
        """Create and return an ncurses window wrapper of dimensions = (rows, colums)."""
        rows, columns = dimensions

        # Writing to the last cell of a window raises an exception because the
        # automatic cursor move to the next cell is illegal which is an ncurses
        # limitation. The +1 to rows fixes that without impacting most anything
        # else. The one thing it affects is there's a line after the last
        # application line where writes don't explicitely error out.
        window = curses.newpad(rows + 1, columns)
        return NCursesWindow(window)

    def flush(self):
        curses.doupdate()

    def suspend(self):
        curses.def_prog_mode()
        curses.reset_shell_mode()
        curses.endwin()

    def resume(self):
        curses.reset_prog_mode()


class NCursesWindow(object):

    _root_win = None
    _color_map = None
    _encoding = None
    _key_map = ncurses_key_map
    IMPLEMENTATION = GAME.NCURSES

    @classmethod
    def init_class_attributes(cls, curses_root_window=None):
        """
        Initialize curses if not already and prepare class attributes.

        This function has to be called separately if this class is used directly
        instead from NCursesWrapper().new_window(dimensions).
        """
        cls._encoding = locale.getpreferredencoding()
        cls._root_win = cls(_init_curses(curses_root_window))

        if curses.COLORS == 256:
            cls._color_map = NCurses256ColorDict()
        else:
            cls._color_map = NCursesColorDict()

    def __init__(self, curses_window):
        self.win = curses_window
        self.win.keypad(True)
        self.win.immedok(False)
        self.win.scrollok(False)

    def addch(self, y, x, char):
        symbol, color = char
        self.win.addch(y, x, symbol.encode(self._encoding), self._color_map[color])

    def addstr(self, y, x, string, color=None):
        if color is None:
            self.win.addstr(y, x, string.encode(self._encoding))
        else:
            self.win.addstr(y, x, string.encode(self._encoding), self._color_map[color])

    def draw(self, char_payload_sequence):
        d = self.win.addch
        local_color = self._color_map
        for y, x, (symbol, color) in char_payload_sequence:
            d(y, x, symbol.encode(self._encoding), local_color[color])

    def draw_reverse(self, char_payload_sequence):
        d = self.win.addch
        local_color = self._color_map
        for y, x, (symbol, (fg, bg)) in char_payload_sequence:
            d(y, x, symbol.encode(self._encoding), local_color[bg, fg])

    def clear(self):
        self.win.erase()

    def blit(self, size, screen_position):
        self._check_root_window_size()
        rows, cols = size
        y, x = screen_position
        self.win.noutrefresh(0, 0, y, x, y + rows - 1, x + cols - 1)

    def get_dimensions(self):
        return self.win.getmaxyx()

    def move(self, y, x):
        self.win.move(y, x)

    def get_cursor_pos(self):
        return self.win.getyx()

    def get_key(self):
        return self._interpret_ch(self._esc_key_handler(self.win.getch()))

    def check_key(self):
        """Non-blocking version of get_key."""
        self.win.nodelay(True)
        ch = self.get_key()
        self.win.nodelay(False)
        if ch != curses.ERR:
            return ch
        else:
            return KEY.NO_INPUT

    def _interpret_ch(self, ch):

        if ch == curses.KEY_RESIZE:
            self._check_root_window_size()
        elif ch in self._key_map:
            ch = self._key_map[ch]
        else:
            ch = curses.ascii.unctrl(ch)
            if '^' in ch:
                ch = ch.lower()

        if debug.show_keycodes and ch != KEY.NO_INPUT:
            logging.debug("User input: {}".format(ch))

        return ch

    def _esc_key_handler(self, ch):
        if ch == curses.ascii.ESC:
            self.win.nodelay(True)
            second_ch = self.win.getch()
            self.win.nodelay(False)
            if second_ch != curses.ERR:
                return curses.ascii.alt(second_ch)
        return ch

    @classmethod
    def _check_root_window_size(cls):
        rows, cols = cls._root_win.get_dimensions()
        while rows < GAME.SCREEN_ROWS or cols < GAME.SCREEN_COLS:
            message = ("Game needs at least a screen size of {}x{} while the "
                       "current size is {}x{}. Please resize the screen or "
                       "press Q to quit.")
            message = message.format(GAME.SCREEN_COLS, GAME.SCREEN_ROWS, cols, rows)
            cls._root_win.addstr(0, 0, message.encode(cls._encoding))
            cls._root_win.win.refresh()

            if cls._root_win.get_key() == "Q":
                cls._root_win.clear()
                message = "Confirm quit by pressing Y."
                cls._root_win.addstr(0, 0, message.encode(cls._encoding))
                cls._root_win.win.refresh()
                if cls._root_win.get_key() == "Y":
                    exit()
            cls._root_win.clear()
            cls._root_win.win.refresh()
            rows, cols = cls._root_win.get_dimensions()
