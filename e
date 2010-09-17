#!/usr/bin/env python

from curses import wrapper
from cPickle import load
from os import path

def main(w):
	import io
	import tile

	io.io = io.IO(w)
	#with open(path.join("data", "tiles"), "r") as f:
	#	tile.tiles = load(f)
	from editor import Editor
	Editor()

wrapper(main)
