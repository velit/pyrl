from __future__ import with_statement
import pickle
import os
import const.game as GAME

from io import open
from pio import init_global_io


def curses_inited_main(w, options):
	import window.curses_window as curses_window
	curses_window.init_module()
	init_global_io(curses_window.CursesWindow, w)
	start(options)

def tcod_main(options):
	import window.tcod_window as tcod_window
	tcod_window.init_module()
	init_global_io(tcod_window.TCODWindow, None)
	start(options)

def start(options):
	from pio import io
	if io.rows < GAME.MIN_SCREEN_ROWS or io.cols < GAME.MIN_SCREEN_COLS:
		message = "Current screen size {}x{} is too small. Needs to be at least {}x{}"
		io.notify(message.format(io.cols, io.rows, GAME.MIN_SCREEN_COLS, GAME.MIN_SCREEN_ROWS))
		exit()

	from game import Game

	if options.load:
		game = load("pyrl.svg")
		game.register_status_texts()
		game.redraw()
	else:
		game = Game()

	while True:
		game.play()

def load(name):
	with open(os.path.join("data", name), "rb") as f:
		return pickle.load(f)
