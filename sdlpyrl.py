#!/usr/bin/env python

import argparse
import cProfile
import main


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--load", action="store_true")
parser.add_argument("-p", "--profile", action="store_true")

options = parser.parse_args()

if options.profile:
	cProfile.run("main.tcod_main(options)", "profiler_data")
else:
	main.tcod_main(options)
