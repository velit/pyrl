#!/usr/bin/env python
try:
	import curses
except ImportError:
	print("Couldn't import curses. Try running sdlpyrl.py")
	exit()

import main
import wrapper_ncurses

def start(curses_window):
	main.set_cursor_library(wrapper_ncurses, curses_window)
	main.start()

curses.wrapper(start)
