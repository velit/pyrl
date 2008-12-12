import sys
import curses
import pickle

from game import Game

def main(w):
	if len(sys.argv) == 2:
		game = pickle.load(open("pyrl.svg", "r"))
		IO(game.ydelta, game.xdelta)
		game.cur_level.refresh()
	else:
		game = Game(w)

	while True:
		game.play()
curses.wrapper(main)
