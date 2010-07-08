#!/usr/bin/env python

from curses import wrapper
from cPickle import load
from os import path

def main(w):
	import io
	import tile

	f = open(path.join("data", "tiles"), "r")
	io.io = io.IO(w)
	tile.tiles = load(f)
	f.close()
	from editor import Editor
	Editor()

wrapper(main)
