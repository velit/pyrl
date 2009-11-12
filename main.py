import curses

def main(w):
	from game import Game
	
	game = Game()

	while True:
		game.play()

curses.wrapper(main)
