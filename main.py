import sys
import pickle
import curses
import os
import const.game as CG

from game import Game
from pio import init_io_module, io


class Main:

	def __init__(self, w, load):
		init_io_module(w)
		if io.rows < CG.MIN_SCREEN_ROWS or io.cols < CG.MIN_SCREEN_COLS:
			message = "Current screen size {}x{} is too small. Needs to be at least {}x{}"
			io.sel_getch(message.format(io.cols, io.rows, CG.MIN_SCREEN_COLS, CG.MIN_SCREEN_ROWS))
			exit()
		elif load:
			self.load()
		else:
			self.game = Game()

	def start(self):
		while True:
			self.game.play()

	def load(self):
		with open(os.path.join("data", "pyrl.svg"), "rb") as f:
			self.game = pickle.load(f)
			self.game.register_status_texts()
			self.game.redraw()


def wrap(w):
	load = (len(sys.argv) == 2 and sys.argv[1] == "load")
	m = Main(w, load)
	m.start()


curses.wrapper(wrap)
