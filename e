#!/usr/bin/env python

from curses import wrapper
from cPickle import load
from os import path
#import curses

def main(w):
	import io

	io.io = io.IO(w)
	from editor import Editor
	Editor()

wrapper(main)

#w = curses.initscr()
#curses.noecho()
#curses.cbreak()
#w.keypad(1)
#curses.start_color()

#try:
#	main(w)
#except:
#	curses.nocbreak()
#	w.keypad(0)
#	curses.echo()
#	curses.endwin()
#	raise
