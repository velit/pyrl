#!/usr/bin/env python

import argparse
import cProfile
import main


parser = argparse.ArgumentParser()
parser.add_argument(u"-l", u"--load", action=u"store_true")
parser.add_argument(u"-p", u"--profile", action=u"store_true")

options = parser.parse_args()

try:
	import curses
except ImportError:
	print("Couldn't import curses. Try the libtcod version with ./tcodpyrl.py")

if options.profile:
	cProfile.run(u"curses.wrapper(main.curses_inited_main, options)", u"profiler_data")
else:
	curses.wrapper(main.curses_inited_main, options)
