#!/usr/bin/env python

from curses import wrapper

def main(w):
	import io

	io.io = io.IO(w)
	from editor import Editor
	Editor()

wrapper(main)
