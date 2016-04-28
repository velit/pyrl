#!/usr/bin/env python3
import main
from io_wrappers.curses import CursesWrapper, clean_curses


try:
    main.start(CursesWrapper)
finally:
    clean_curses()
