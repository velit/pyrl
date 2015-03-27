#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function, unicode_literals

import main
from io_wrappers.ncurses import NCursesWrapper


try:
    main.start(NCursesWrapper)
finally:
    if NCursesWrapper.is_ncurses_init():
        NCursesWrapper.suspend()
