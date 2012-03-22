import argparse
import cProfile
import state_store
import const.game as GAME


cursor_lib = None
io = None

def set_cursor_library(cursor_library):
	global cursor_lib, io
	cursor_lib = cursor_library

	from window.window_system import WindowSystem
	io = WindowSystem(cursor_lib.get_root_window())


def start():
	cursor_lib.init()
	root_window = cursor_lib.get_root_window()

	# check to see the window is big enough
	window_rows, window_cols = cursor_lib.get_dimensions(root_window)
	if window_rows < GAME.MIN_SCREEN_ROWS or window_cols < GAME.MIN_SCREEN_COLS:
		raw_message = "Current screen size {}x{} is too small. Needs to be at least {}x{}"
		message = raw_message.format(window_cols, window_rows, GAME.MIN_SCREEN_COLS, GAME.MIN_SCREEN_ROWS)
		cursor_lib.addstr(root_window, 0, 0, message)
		cursor_lib.get_key(root_window)
		exit()

	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--load", action="store_true")
	parser.add_argument("-p", "--profile", action="store_true")
	options = parser.parse_args()

	from game import Game

	if options.load:
		game = load("pyrl.svg")
		game.register_status_texts(game.player)
		game.redraw()
	else:
		game = Game()

	if options.profile:
		cProfile.run("play(game)")
	else:
		play(game)


def play(game):
	while True:
		game.play()


def load(name):
	return state_store.load(name)
