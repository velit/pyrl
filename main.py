import sys
import pickle
import curses
import os

from game import Game
from pio import init_io_module


class Main:

	def __init__(self, w, load):
		init_io_module(w)
		if load:
			self.load()
		else:
			self.game = Game(self)

	def start(self):
		while True:
			self.game.play()

	def load(self):
		with open(os.path.join("data", "pyrl.svg"), "rb") as f:
			self.game = pickle.load(f)
			self.game.redraw()
			self.game.p.register_status_texts()


def wrap(w):
	load = (len(sys.argv) == 2 and sys.argv[1] == "-l")
	m = Main(w, load)
	m.start()


curses.wrapper(wrap)
