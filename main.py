import sys
import curses
import cPickle

from os import path

class Main(object):
	def __init__(self, w, load):
		import io
		import tile
		
		io.io = io.IO(w, 2, 2)

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
	if len(sys.argv) == 2 and sys.argv[1] == "-l":
		load = True
	else:
		load = False
	m = Main(w, load)

	while True:
		m.play()

curses.wrapper(main)
