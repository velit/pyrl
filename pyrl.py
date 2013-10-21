#!/usr/bin/env python
try:
    import curses
except ImportError:
    print("Couldn't import curses. Try running sdlpyrl.py")
    exit()

import main
import wrapper_ncurses


def start(curses_window):
    wrapper_ncurses.init(curses_window)
    main.init_window_system(wrapper_ncurses)
    main.start()

curses.wrapper(start)
