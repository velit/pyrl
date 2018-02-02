try:
    import curses
except ImportError:
    import sys
    print("Couldn't import curses. Try running sdlpyrl.py")
    sys.exit(1)

import curses.ascii
import logging

from pyrl.config.debug import Debug
from pyrl.enums.keys import Key
from pyrl.io_wrappers.curses_dicts import Curses256ColorDict, CursesColorDict, curses_key_map
from pyrl.window.window_system import WindowSystem


IMPLEMENTATION = "curses"


def clean_curses():
    """Resume normal shell state. Does nothing if curses wasn't initialized."""
    try:
        curses.reset_shell_mode()
    except curses.error:
        pass
    try:
        curses.endwin()
    except curses.error:
        pass


class CursesWrapper(object):

    implementation = IMPLEMENTATION

    def __init__(self, curses_root_window=None):
        """Initialize curses and prepare for creation of new windows."""
        if curses_root_window is None:
            curses_root_window = curses.initscr()
        self.curses_root_window = curses_root_window

        curses.noecho()
        curses.cbreak()                   # no line buffering
        curses.nonl()                     # allow return key detection in input
        curses.curs_set(0)                # Remove cursor visibility
        curses_root_window.keypad(True)

        # see curses.wrapper implementation for reason for try-except
        try:
            curses.start_color()
        except:
            pass

        self.root_win = CursesWindow(self.curses_root_window)

    def new_window(self, dimensions):
        """Create and return an curses window wrapper of dimensions = (rows, colums)."""
        rows, columns = dimensions

        # Writing to the last cell of a window raises an exception because the
        # automatic cursor move to the next cell is illegal which is a curses
        # limitation. The +1 to rows fixes that without impacting most anything
        # else. The one thing it affects is there's a line after the last
        # application line where writes don't explicitely error out.
        window = curses.newpad(rows + 1, columns)
        return CursesWindow(window, self.root_win)

    def flush(self):
        curses.doupdate()

    def suspend(self):
        curses.def_prog_mode()
        curses.reset_shell_mode()
        curses.endwin()

    def resume(self):
        curses.reset_prog_mode()


class CursesWindow(object):

    implementation = IMPLEMENTATION
    color_map = None
    key_map = curses_key_map

    def __init__(self, curses_window, root_window=None):
        if root_window is None:
            self.root_win = self
        else:
            self.root_win = root_window

        if self.color_map is None:
            if curses.COLORS == 256:
                CursesWindow.color_map = Curses256ColorDict()
            else:
                CursesWindow.color_map = CursesColorDict()

        self.win = curses_window
        self.win.keypad(True)
        self.win.immedok(False)
        self.win.scrollok(False)

    def draw_char(self, char, coord=(0, 0)):
        y, x = coord
        symbol, color = char
        self.win.addstr(y, x, symbol, self.color_map[color])

    def draw_str(self, string, coord=(0, 0), color=None):
        y, x = coord
        if color is None:
            self.win.addstr(y, x, string)
        else:
            self.win.addstr(y, x, string, self.color_map[color])

    def draw(self, char_payload_sequence):
        local_addch = self.win.addstr
        local_color = self.color_map
        for (y, x), (symbol, color) in char_payload_sequence:
            local_addch(y, x, symbol, local_color[color])

    def draw_reverse(self, char_payload_sequence):
        local_addch = self.win.addstr
        local_color = self.color_map
        for (y, x), (symbol, (fg, bg)) in char_payload_sequence:
            local_addch(y, x, symbol, local_color[bg, fg])

    def clear(self):
        self.win.erase()

    def blit(self, size, screen_position):
        self._ensure_terminal_is_big_enough()
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
        while True:
            try:
                ch = self.win.get_wch()
                break
            except curses.error as err:
                if err.args == ("no input", ):
                    continue
                else:
                    raise
        return self._interpret_ch(*self._handle_alt(ch))

    def get_key_unguarded(self):
        return self._interpret_ch(*self._handle_alt(self.win.get_wch()))

    def check_key(self):
        """Non-blocking version of get_key."""
        self.win.nodelay(True)
        try:
            return self.get_key_unguarded()
        except curses.error as err:
            if err.args == ("no input", ):
                return Key.NO_INPUT
            else:
                raise
        finally:
            self.win.nodelay(False)

    def _interpret_ch(self, key, alt):

        if Debug.show_keycodes and key != Key.NO_INPUT:
            raw = key

        if key == curses.KEY_RESIZE:
            self._ensure_terminal_is_big_enough()

        if key in self.key_map:
            key = self.key_map[key]
        elif isinstance(key, int):
            key = str(key)
        else:
            nr = ord(key)
            if nr < 128:
                key = alt * "!" + curses.ascii.unctrl(key)
                if "^" in key:
                    key = key.lower()
            else:
                key = alt * "!" + key

        if Debug.show_keycodes and key != Key.NO_INPUT:
            logging.debug("User input: raw: {} interp: {}{}".format(raw, key, " alt:yes" * alt))

        return key

    def _handle_alt(self, key):
        alt = False
        if key == chr(curses.ascii.ESC):
            second_key = self.check_key()
            if second_key != Key.NO_INPUT:
                key = second_key
                alt = True
        return key, alt

    def _ensure_terminal_is_big_enough(self):
        rows, cols = self.root_win.get_dimensions()
        min_rows, min_cols = WindowSystem.game_dimensions
        while rows < min_rows or cols < min_cols:
            message = ("Game needs at least a screen size of {}x{} while the "
                    "current size is {}x{}. Please resize the screen or "
                    "press Q to quit.")
            message = message.format(min_cols, min_rows, cols, rows)
            self.root_win.draw_str(message)
            self.root_win.win.refresh()

            if self.root_win.get_key() == "Q":
                self.root_win.clear()
                message = "Confirm quit by pressing Y."
                self.root_win.draw_str(message)
                self.root_win.win.refresh()
                if self.root_win.get_key() == "Y":
                    exit()
            self.root_win.clear()
            self.root_win.win.refresh()
            rows, cols = self.root_win.get_dimensions()
