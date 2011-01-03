import sys
import curses
import cPickle as pickle

from os import path
from constants import STATUS_BAR_SIZE, MSG_BAR_SIZE

class Main(object):
	def __init__(self, w, load):
		import io
		io.io = io.IO(w, STATUS_BAR_SIZE, MSG_BAR_SIZE)
		from game import Game
		if load:
			self.load()
		else:
			self.game = Game()

	def play(self):
		self.game.play()

	def load(self):
		with open(path.join("data", "pyrl.svg"), "r") as f:
			self.game = pickle.load(f)
			self.game.redraw()

def main(w):
	load = (len(sys.argv) == 2 and sys.argv[1] == "-l")
	m = Main(w, load)

	while True:
		m.play()

curses.wrapper(main)
