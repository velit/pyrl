from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import atexit
import locale
import logging
import sys
import os
from cProfile import Profile

import state_store
from config.game import GameConf
from config.debug import Debug
from tools import profile_util


def start(cursor_lib_callback):
    game = prepare_game(cursor_lib_callback)
    game.main_loop()


def prepare_game(cursor_lib_callback, cmdline_args=None):

    options = get_commandline_options(cmdline_args)
    initialize_files_and_folders()

    locale.setlocale(locale.LC_ALL, "")
    init_logger_system()

    if options.load:
        game = load_game(options.load, cursor_lib_callback)
    else:
        from game import Game
        game = Game(options.game, cursor_lib_callback)

    if options.profile:
        profiler = Profile()
        profiler.enable()

        def write_profile():
            profiler.disable()
            profile_util.write_results_log(profiler)

        atexit.register(write_profile)

    return game


def init_logger_system():
    logging.basicConfig(filename=Debug.log_file, level=Debug.log_level)


def get_commandline_options(args=None):

    parser = argparse.ArgumentParser(description="pyrl; Python Roguelike")
    start_group = parser.add_mutually_exclusive_group()
    start_group.add_argument("-g", "--game", help="Specify the name for a new game.",
                             nargs="?", const=GameConf.default_game_name, default=GameConf.default_game_name)
    start_group.add_argument("-l", "--load", help="Specify the game to be loaded.", nargs="?", const=GameConf.default_game_name)
    parser.add_argument("-p", "--profile", help="Generate profiling data during the game.", action="store_true")

    return parser.parse_args(args)


def load_game(game_name, cursor_lib_callback):
    try:
        game = state_store.load(game_name)
    # python3: use FileNotFoundError here instead
    except IOError:
        print("Game '{}' not found.".format(game_name), file=sys.stderr)
        sys.exit(1)
    game.init_nonserial_objects(cursor_lib_callback)
    game.redraw()
    return game


def initialize_files_and_folders():
    if not os.path.exists(GameConf.DATA_FOLDER):
        os.makedirs(GameConf.DATA_FOLDER)
