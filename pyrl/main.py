from __future__ import annotations

import argparse
import atexit
import logging
import os
import sys
from cProfile import Profile
from collections.abc import Sequence

from pyrl import state_store
from pyrl.config.config import Config
from pyrl.config.debug import Debug
from pyrl.game import Game
from pyrl.io_wrappers.io_wrapper import IoWrapper
from tools import profile_util


def run() -> None:
    options = get_commandline_options()
    try:
        create_game(options).game_loop()
    finally:
        if options.output == "terminal":
            from pyrl.io_wrappers.curses import clean_curses
            clean_curses()

def get_commandline_options(args: Sequence[str] | None = None) -> argparse.Namespace:
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

def create_game(options: argparse.Namespace, cursor_lib: IoWrapper | None = None) -> Game:
    init_files_and_folders()
    init_logger_system()

    if cursor_lib is None:
        cursor_lib = init_cursor_lib(options.output)

    if options.load:
        game = load_game(options.load, cursor_lib)
    else:
        game = Game(options.game, cursor_lib)

    if options.profile:
        profiler = Profile()
        profiler.enable()

        def write_profile() -> None:
            profiler.disable()
            profile_util.write_results_log(profiler)

        atexit.register(write_profile)

    return game

def init_logger_system() -> None:
    logging.basicConfig(filename=Debug.log_file, level=Debug.log_level)
    logging.debug("Starting new session")

def init_cursor_lib(output: str) -> IoWrapper:
    if output == "terminal":
        from pyrl.io_wrappers.curses.curses_wrapper import CursesWrapper
        return CursesWrapper()
    elif output == "sdl":
        from pyrl.io_wrappers.tcod.tcod_wrapper import TCODWrapper
        return TCODWrapper()
    elif output == "test":
        from pyrl.io_wrappers.mock.mock_wrapper import MockWrapper
        return MockWrapper()
    else:
        assert False, f"Unknown output parameter '{output}'"

def load_game(game_name: str, cursor_lib: IoWrapper) -> Game:
    try:
        game = state_store.load(game_name)
    except FileNotFoundError:
        print(f"Save file '{game_name}' not found.", file=sys.stderr)
        sys.exit(1)
    game.init_nonserialized_state(cursor_lib)
    game.redraw()
    return game

def init_files_and_folders() -> None:
    if not os.path.exists(Config.save_folder):
        os.makedirs(Config.save_folder)
