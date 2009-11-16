import curses

def main(w):
	from io import io
	from game import Game
	
	game = Game()

	while True:
		game.play()

curses.wrapper(main)
