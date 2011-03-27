from curses import wrapper
from editor import Editor
from pio import init_io_module


def main(w):
	init_io_module(w)
	Editor()

wrapper(main)
