try:
	import sys
	import curses
	import pickle

	from io import IO
	from game import Game

	def main(w):
		
		game = Game(w)

		while True:
			game.play()

	curses.wrapper(main)
finally:
	curses.nocbreak()
	curses.echo()
	curses.initscr().keypad(0)
	curses.endwin()
