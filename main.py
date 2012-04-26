import argparse
import cProfile
import state_store
from const.game import NCURSES


cursor_lib = None
io = None
root_win = None


def set_cursor_library(cursor_library, root_window):
    global cursor_lib, io, root_win
    cursor_lib = cursor_library
    root_win = root_window

    from window.window_system import WindowSystem
    io = WindowSystem(cursor_lib.get_root_window())


def start():
    cursor_lib.init(root_win)
    if cursor_lib.get_implementation() == NCURSES:
        # check to see the window is big enough
        cursor_lib._window_resized()

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
