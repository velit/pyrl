from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import logging
from cProfile import Profile

import profile_util
import state_store
from const.game import LOG_FILE, LOG_LEVEL
from window.window_system import WindowSystem


# Global object for the input and output window system
# Check the WindowSystem class for the implementation
io = None


def init_window_system(cursor_library):
    global io
    io = WindowSystem(cursor_library)


def init_logger_system():
    logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL)


def start():

    init_logger_system()

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
        profiler = Profile()
        profiler.enable()

    game.main_loop()

    if options.profile:
        profiler.disable()
        profile_util.write_profile_results(profiler)


def load(name):
    return state_store.load(name)
