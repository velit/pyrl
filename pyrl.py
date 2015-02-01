#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import main
import wrapper_ncurses


try:
    import curses
except ImportError:
    print("Couldn't import curses. Try running sdlpyrl.py")
    exit()


def start(curses_window):
    wrapper_ncurses.init(curses_window)
    main.init_window_system(wrapper_ncurses)
    main.start()


curses.wrapper(start)
