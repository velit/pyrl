from __future__ import annotations

import argparse
import atexit
import logging
import os
import secrets
import sys
from cProfile import Profile
from collections.abc import Sequence

from pyrl.config.binds import Binds
from pyrl.config.config import Config
from pyrl.config.debug import Debug
from pyrl.engine import state_store
from pyrl.engine.game import Game
from pyrl.ui.io_lib.protocol.io_wrapper import IoWrapper
from pyrl.ui.views.line import from_multiline_str
from pyrl.ui.window.window_system import WindowSystem
from tools import profile_util

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

def main() -> None:
    options = get_commandline_options()
    init_files_and_folders()
    init_logger_system(options.output)
    with init_cursor_lib(options.output) as io_wrapper:
        init_game(options, WindowSystem(io_wrapper)).game_loop()

def init_game(options: argparse.Namespace, window_system: WindowSystem) -> Game:
    if options.load:
        game = load_game(options.load, window_system)
    else:
        game = Game(options.game, window_system)

    if options.profile:
        profiler = Profile()
        profiler.enable()

        def write_profile() -> None:
            profiler.disable()
            profile_util.write_results_log(profiler, "game_profile.log")

        atexit.register(write_profile)

    return game

def load_game(game_name: str, io: WindowSystem) -> Game:
    try:
        game = state_store.load(game_name)
    except FileNotFoundError:
        print(f"Save file '{game_name}' not found.", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        show_load_warning(io)
        game = state_store.load(game_name, unsafe=True)
    assert isinstance(game, Game), f"Loaded data isn't a savegame. Found an object of type {type(game)}"
    game.init_non_serialized_state(io)
    game.redraw()
    return game

def init_files_and_folders() -> None:
    Config.save_folder.mkdir(parents=True, exist_ok=True)

def init_logger_system(output: str) -> None:
    if output == "sdl":
        logging.basicConfig(level=Debug.log_level)
        logging.debug("Starting new session")
    else:
        logging.basicConfig(filename=Debug.log_file, level=Debug.log_level)
        logging.debug("Starting new session")

def init_cursor_lib(output: str) -> IoWrapper:
    if output == "terminal":
        from pyrl.ui.io_lib.curses.curses_wrapper import CursesWrapper
        return CursesWrapper()
    elif output == "sdl":
        from pyrl.ui.io_lib.tcod.tcod_wrapper import TcodWrapper
        return TcodWrapper()
    elif output == "test":
        from pyrl.ui.io_lib.mock.mock_wrapper import MockWrapper
        return MockWrapper()
    else:
        assert False, f"Unknown output parameter '{output}'"

def show_load_warning(io: WindowSystem) -> None:
    raw_warning = f"""
                                     WARNING APPROACHING

 ********************************************************************************************** 
 *                                                                                            * 
 *               The save functionality of this game is implemented using pickle.             * 
 *                       https://docs.python.org/3/library/pickle.html                        * 
 *                      Pickle is vulnerable to arbitrary code execution.                     * 
 *                                                                                            * 
 *                         ONLY USE SAVE FILES FROM SOURCES YOU TRUST!                        * 
 *                                                                                            * 
 *        This warning is shown because an attempt is made to track the origin of saves.      * 
 *            The detection isn't perfect and this warning can be shown erroneously.          * 
 *       This warning can be disabled by setting Save_Game_Warning = false in config.toml.    * 
 *                                                                                            * 
 ********************************************************************************************** 

                   Press [{Binds.Yes}] to continue, anything else to abort:"""

    io.whole_window.draw_lines(from_multiline_str(raw_warning))
    if io.whole_window.get_key(refresh=True) not in Binds.Yes:
        sys.exit(0)
