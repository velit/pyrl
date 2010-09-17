import sys
import curses
import cPickle

from os import path
from constants import STATUS_BAR_SIZE, MSG_BAR_SIZE, TILES_LOADED_FROM_FILE

class Main(object):
	def __init__(self, w, load):
		import io
		io.io = io.IO(w, STATUS_BAR_SIZE, MSG_BAR_SIZE)

		import tile
		if TILES_LOADED_FROM_FILE:
			with open(path.join("data", "tiles"), "r") as f:
				tile.tiles = cPickle.load(f)
		
		from game import Game
		if load:
			self.load()
		else:
			self.game = Game(self)

	def play(self):
		self.game.play()

	def load(self):
		with open(path.join("data", "pyrl.svg"), "r") as f:
			self.game = cPickle.load(f)
			self.game.redraw()

def main(w):
	load = (len(sys.argv) == 2 and sys.argv[1] == "-l")
	m = Main(w, load)

	while True:
		m.play()

curses.wrapper(main)
