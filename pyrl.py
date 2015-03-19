#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import main
from wrapper_ncurses import NCursesWrapper


try:
    import curses
except ImportError:
    print("Couldn't import curses. Try running sdlpyrl.py")
    exit()


def start(curses_window):

    main.init_window_system(NCursesWrapper(curses_window))
    main.start()


curses.wrapper(start)
