import pickle
import os
import const.game as GAME

from pio import init_io_module


def curses_inited_main(w, options):
	init_io_module(w)
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
