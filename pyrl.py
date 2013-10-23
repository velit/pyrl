#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


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
