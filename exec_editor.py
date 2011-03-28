from curses import wrapper
from pio import init_io_module
from editor.main import Editor


def main(w):
	init_io_module(w)
	Editor()

wrapper(main)
