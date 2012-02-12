#!/usr/bin/env python

import argparse
import cProfile
import main


parser = argparse.ArgumentParser()
parser.add_argument(u"-l", u"--load", action=u"store_true")
parser.add_argument(u"-p", u"--profile", action=u"store_true")

options = parser.parse_args()

if options.profile:
	cProfile.run(u"main.tcod_main(options)", u"profiler_data")
else:
	main.tcod_main(options)
