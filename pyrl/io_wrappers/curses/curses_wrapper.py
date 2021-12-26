from __future__ import annotations

import curses

from pyrl.io_wrappers.curses import IMPLEMENTATION
from pyrl.io_wrappers.curses.curses_window import CursesWindow
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.structures.dimensions import Dimensions

class CursesWrapper(IoWrapper):

    implementation = IMPLEMENTATION

    def __init__(self) -> None:
        """Initialize curses and prepare for creation of new windows."""
        self.curses_root_window = curses.initscr()

        curses.noecho()
        curses.cbreak()                   # no line buffering
        curses.nonl()                     # allow return key detection in input
        curses.curs_set(0)                # Remove cursor visibility
        self.curses_root_window.keypad(True)

        # see curses.wrapper implementation for reason for try-except
        # noinspection PyBroadException
        try:
            curses.start_color()
        except:
            pass

        self.root_win = CursesWindow(self.curses_root_window)

    def new_window(self, dimensions: Dimensions) -> IoWindow:
        """Create and return a curses window wrapper of dimensions = (rows, colums)."""
        rows, columns = dimensions.params

        # Writing to the last cell of a window raises an exception because the
        # automatic cursor move to the next cell is illegal which is a curses
        # limitation. The +1 to rows fixes that without impacting most anything
        # else. The one thing it affects is there's a line after the last
        # application line where writes don't explicitely error out.
        window = curses.newpad(rows + 1, columns)
        return CursesWindow(window, self.root_win)

    def flush(self) -> None:
        curses.doupdate()

    def suspend(self) -> None:
        curses.def_prog_mode()
        curses.reset_shell_mode()
        curses.endwin()

    def resume(self) -> None:
        curses.reset_prog_mode()
