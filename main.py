import const.game as GAME
import input_output
import state_store

def curses_inited_main(w, options):
	import wrapper_curses

	wrapper_curses.init()

	input_output.io = input_output.Front(wrapper_curses, w)

	start(options)

def tcod_main(options):
	import wrapper_libtcod

	wrapper_libtcod.init()

	input_output.io = input_output.Front(wrapper_libtcod, 0)

	start(options)

def start(options):
	io = input_output.io
	if io.rows < GAME.MIN_SCREEN_ROWS or io.cols < GAME.MIN_SCREEN_COLS:
		message = "Current screen size {}x{} is too small. Needs to be at least {}x{}"
		io.notify(message.format(io.cols, io.rows, GAME.MIN_SCREEN_COLS, GAME.MIN_SCREEN_ROWS))
		exit()

	from game import Game

	if options.load:
		game = load("pyrl.svg")
		game.register_status_texts(game.player)
		game.redraw()
	else:
		game = Game()

	while True:
		game.play()

def load(name):
	return state_store.load(name)
