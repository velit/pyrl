#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function, unicode_literals

import main
from io_wrappers.curses import CursesWrapper, clean_curses


try:
    main.start(CursesWrapper)
finally:
    clean_curses()
