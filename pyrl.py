#!/usr/bin/env python
from pyrl import main
from pyrl import wrapper_ncurses


try:
    import curses
except ImportError:
    print("Couldn't import curses. Try running sdlpyrl.py")
    exit()


def start(curses_window):
    main.set_cursor_library(wrapper_ncurses, curses_window)
    main.start()

curses.wrapper(start)
