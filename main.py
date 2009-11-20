import curses

def main(w):
	import io
	io.io = io.IO(w, 2, 2)
	
	from game import Game
	game = Game()

	while True:
		game.play()

curses.wrapper(main)
