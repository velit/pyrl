from __future__ import annotations

import tcod

from pyrl.config.config import Config
from pyrl.structures.dimensions import Dimensions
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.tcod import IMPLEMENTATION
from pyrl.io_wrappers.tcod.tcod_window import TcodWindow
from pyrl.window.window_system import WindowSystem

class TCODWrapper(IoWrapper):
    """Wrapper for the chronicles of doryen roguelike library (SDL)."""

    implementation = IMPLEMENTATION

    def __init__(self) -> None:
        """Init the SDL surface and prepare for draw calls."""
        flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
        tcod.console_set_custom_font(b"resources/terminal10x18_gs_ro.png", flags)
        rows, cols = WindowSystem.game_dimensions.params
        tcod.console_init_root(cols, rows, Config.default_game_name, False, tcod.RENDERER_SDL)

    def new_window(self, dimensions: Dimensions) -> IoWindow:
        rows, columns = dimensions.params
        console = tcod.console_new(columns, rows)
        return TcodWindow(console)

    def flush(self) -> None:
        tcod.console_flush()

    def suspend(self) -> None:
        """SDL version doesn't require suspend."""
        pass

    def resume(self) -> None:
        """SDL version doesn't require resume."""
        pass

    def _toggle_fullscreen(self) -> None:
        if tcod.console_is_fullscreen():
            tcod.console_set_fullscreen(False)
        else:
            tcod.console_set_fullscreen(True)
