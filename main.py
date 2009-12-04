import curses
from pickle import load

def main(w):
	import io
	import tile

	f = open("data", "r")

	io.io = io.IO(w, 2, 2)
	tile.tiles = load(f)

	f.close()
	
	from game import Game
	game = Game()

	while True:
		game.play()

curses.wrapper(main)
