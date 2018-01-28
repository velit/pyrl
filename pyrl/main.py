import argparse
import atexit
# import locale
import logging
import os
import sys
from cProfile import Profile

from pyrl import state_store
from pyrl.config.debug import Debug
from pyrl.config.game import GameConf
from tools import profile_util


def run():
    options = get_commandline_options()
    try:
        game(options).game_loop()
    finally:
        if options.cursor_lib == "curses":
            from pyrl.io_wrappers.curses import clean_curses
            clean_curses()


def get_commandline_options(args=None):
    parser = argparse.ArgumentParser(description="pyrl; Python Roguelike")

    parser.add_argument("-r", "--renderer",
                        help="Select which renderer to use to display the game.",
                        action="store",
                        dest="cursor_lib",
                        choices=["sdl", "curses"],
                        default="sdl")

    start_type = parser.add_mutually_exclusive_group()
    start_type.add_argument("-g", "--game",
                            help="Specify the name for a new game.",
                            nargs="?",
                            const=GameConf.default_game_name,
                            default=GameConf.default_game_name)

    start_type.add_argument("-l", "--load",
                            help="Specify the game to be loaded.",
                            nargs="?",
                            const=GameConf.default_game_name)

    parser.add_argument("-p", "--profile",
                        help="Generate profiling data during the game.",
                        action="store_true")

    return parser.parse_args(args)


def game(options, cursor_lib=None):
    init_files_and_folders()

    # locale.setlocale(locale.LC_ALL, "")
    init_logger_system()

    if cursor_lib is None:
        cursor_lib = init_cursor_lib(options.cursor_lib)
    if options.load:
        game = load_game(options.load, cursor_lib)
    else:
        from pyrl.game import Game
        game = Game(options.game, cursor_lib)

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
    logging.debug("Starting new session")


def init_cursor_lib(cursor_lib):
    if cursor_lib == "curses":
        from pyrl.io_wrappers.curses import CursesWrapper
        return CursesWrapper()
    elif cursor_lib == "sdl":
        from pyrl.io_wrappers.libtcod import TCODWrapper
        return TCODWrapper()
    elif cursor_lib == "test":
        from pyrl.io_wrappers.mock import MockWrapper
        return MockWrapper()
    else:
        assert False, f"Unknown cursor_lib implementation {options.cursor_lib}"


def load_game(game_name, cursor_lib):
    try:
        game = state_store.load(game_name)
    except FileNotFoundError:
        print("Game '{}' not found.".format(game_name), file=sys.stderr)
        sys.exit(1)
    game.init_nonserialized_state(cursor_lib)
    game.redraw()
    return game


def init_files_and_folders():
    if not os.path.exists(GameConf.save_folder):
        os.makedirs(GameConf.save_folder)
