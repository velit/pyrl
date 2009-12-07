import curses
import cPickle
from os import path

class Main(object):
	def __init__(self, w):
		import io
		import tile
		
		f = open(path.join("data", "tiles") , "r")

		io.io = io.IO(w, 2, 2)
		tile.tiles = cPickle.load(f)

		f.close()
		
		from game import Game
		self.game = Game(self)

	def play(self):
		self.game.play()

	def load(self):
		f = open(path.join("data", "pyrl.svg"), "r")
		self.game = cPickle.load(f)
		f.close()
		self.game.redraw()

def main(w):
	m = Main(w)

	while True:
		m.play()

curses.wrapper(main)
