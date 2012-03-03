import const.game as GAME
import input_output
import state_store

def curses_inited_main(root_window, options):
	import wrapper_ncurses
	wrapper_ncurses.init()
	start(wrapper_ncurses, root_window, options)

def tcod_main(options):
	import wrapper_libtcod
	wrapper_libtcod.init()
	start(wrapper_libtcod, 0, options)

def start(cursor_lib, root_window, options):
	window_rows, window_cols = cursor_lib.get_dimensions(root_window)
	if window_rows < GAME.MIN_SCREEN_ROWS or window_cols < GAME.MIN_SCREEN_COLS:
		raw_message = "Current screen size {}x{} is too small. Needs to be at least {}x{}"
		message = raw_message.format(window_cols, window_rows, GAME.MIN_SCREEN_COLS, GAME.MIN_SCREEN_ROWS)
		cursor_lib.addstr(root_window, 0, 0, message)
		cursor_lib.getch(root_window)
		exit()

	# the input_output module has to be init before the game module is imported
	input_output.init(cursor_lib, root_window)
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
