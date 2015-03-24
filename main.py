from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import atexit
import locale
import logging
from cProfile import Profile

import profile_util
import state_store
from const.game import LOG_FILE, LOG_LEVEL
from window.window_system import WindowSystem


# Global object for the input and output window system
# Check the WindowSystem class for the implementation
#io = None


def init_window_system(cursor_library):
    global io
    io = WindowSystem(cursor_library)


def init_logger_system():
    logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL)


def get_cmdl_args(cmdline_arg_string):

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load", action="store_true")
    parser.add_argument("-p", "--profile", action="store_true")

    return parser.parse_args(cmdline_arg_string)


def prepare_game(cmdline_arg_string=None):

    locale.setlocale(locale.LC_ALL, "")
    init_logger_system()

    options = get_cmdl_args(cmdline_arg_string)

    from game import Game

    if options.load:
        game = state_store.load("pyrl.svg")
        game.register_status_texts(game.player)
        game.redraw()
    else:
        game = Game()

    if options.profile:
        profiler = Profile()
        profiler.enable()

        def write_profile():
            profiler.disable()
            profile_util.write_profile_results(profiler)

        atexit.register(write_profile)

    return game


def start():
    game = prepare_game()
    game.main_loop()
