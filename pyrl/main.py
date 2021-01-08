import argparse
import atexit
import logging
import os
import sys
from cProfile import Profile

from pyrl import state_store
from pyrl.config.config import Config
from pyrl.config.debug import Debug
from tools import profile_util


def run():
    options = get_commandline_options()
    try:
        create_game(options).game_loop()
    finally:
        if options.output == "terminal":
            from pyrl.io_wrappers.curses import clean_curses
            clean_curses()

def get_commandline_options(args=None):
    parser = argparse.ArgumentParser(description="pyrl; Python Roguelike")

    parser.add_argument("-o", "--output",
                        help="Select which output type to run the game in.",
                        action="store",
                        dest="output",
                        choices=["sdl", "terminal"],
                        default="sdl")

    start_type = parser.add_mutually_exclusive_group()
    start_type.add_argument("-g", "--game",
                            help="Specify the name for a new game.",
                            nargs="?",
                            const=Config.default_game_name,
                            default=Config.default_game_name)

    start_type.add_argument("-l", "--load",
                            help="Specify the game to be loaded.",
                            nargs="?",
                            const=Config.default_game_name)

    parser.add_argument("-p", "--profile",
                        help="Generate profiling data during the game.",
                        action="store_true")

    return parser.parse_args(args)

def create_game(options, cursor_lib=None):
    init_files_and_folders()
    init_logger_system()

    if cursor_lib is None:
        cursor_lib = init_cursor_lib(options.output)

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

def init_cursor_lib(output):
    if output == "terminal":
        from pyrl.io_wrappers.curses import CursesWrapper
        return CursesWrapper()
    elif output == "sdl":
        from pyrl.io_wrappers.libtcod import TCODWrapper
        return TCODWrapper()
    elif output == "test":
        from pyrl.io_wrappers.mock import MockWrapper
        return MockWrapper()
    else:
        assert False, f"Unknown output {output}"

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
    if not os.path.exists(Config.save_folder):
        os.makedirs(Config.save_folder)
