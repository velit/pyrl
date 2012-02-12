from __future__ import with_statement
import pickle
import os
import const.game as GAME

from io import open
import input_output

def curses_inited_main(w, options):
	import wrapper_curses

	wrapper_curses.init()

	input_output.io = input_output.Front(wrapper_curses, w)

	start(options)

def tcod_main(options):
	import wrapper_libtcod

	wrapper_libtcod.init()

	input_output.io = input_output.Front(wrapper_libtcod, 0)

	start(options)

def start(options):
	from input_output import io
	if io.rows < GAME.MIN_SCREEN_ROWS or io.cols < GAME.MIN_SCREEN_COLS:
		message = "Current screen size {}x{} is too small. Needs to be at least {}x{}"
		io.notify(message.format(io.cols, io.rows, GAME.MIN_SCREEN_COLS, GAME.MIN_SCREEN_ROWS))
		exit()

	from game import Game

	if options.load:
		game = load("pyrl.svg")
		game.register_status_texts(game.player)
		game.redraw()
	else:
		game = Game()

	while True:
		game.play()

def load(name):
	with open(os.path.join("data", name), "rb") as f:
		return pickle.load(f)
