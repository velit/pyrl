from __future__ import annotations

import curses
import sys
from typing import Any

assert sys.platform != "win32"

from pyrl.engine.structures.dimensions import Dimensions
from pyrl.ui.io_lib.curses import IMPLEMENTATION
from pyrl.ui.io_lib.curses.curses_window import CursesWindow
from pyrl.ui.io_lib.protocol.io_window import IoWindow
from pyrl.ui.io_lib.protocol.io_wrapper import IoWrapper

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

    def __enter__(self) -> IoWrapper:
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self._clean_curses()

    def _clean_curses(self) -> None:
        """Resume normal shell state. Does nothing if curses wasn't initialized."""
        try:
            curses.reset_shell_mode()
        except curses.error:
            pass
        try:
            curses.endwin()
        except curses.error:
            pass

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
