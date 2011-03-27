import sys
import pickle
import curses
import os

from const.game import STATUS_BAR_SIZE, MSG_BAR_SIZE
from game import Game
from pio import init_io_module


class Main():

	def __init__(self, w, load):
		init_io_module(w, STATUS_BAR_SIZE, MSG_BAR_SIZE)
		if load:
			self.load()
		else:
			self.game = Game()

	def play(self):
		self.game.play()

	def load(self):
		with open(os.path.join("data", "pyrl.svg"), "r") as f:
			self.game = pickle.load(f)
			self.game.redraw()


def main(w):
	load = (len(sys.argv) == 2 and sys.argv[1] == "-l")
	m = Main(w, load)

	while True:
		m.play()

curses.wrapper(main)
