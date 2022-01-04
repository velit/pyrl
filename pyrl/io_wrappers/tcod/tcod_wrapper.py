from __future__ import annotations

from typing import Any

import tcod

from pyrl.config.config import Config
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.io_wrappers.tcod import IMPLEMENTATION
from pyrl.io_wrappers.tcod.tcod_tilesets import get_tileset_by_index, get_bdf_index_and_tileset, \
    get_bdf_tileset_by_index
from pyrl.io_wrappers.tcod.tcod_window import TcodWindow
from pyrl.structures.dimensions import Dimensions
from pyrl.window.window_system import WindowSystem


class TcodWrapper(IoWrapper):
    """Wrapper for the chronicles of doryen roguelike library (SDL)."""

    implementation = IMPLEMENTATION

    def __init__(self) -> None:
        """Init the SDL surface and prepare for draw calls."""
        rows, cols = WindowSystem.game_dimensions.params
        # self.tileset_index, tileset = get_index_and_tileset("terminal10x18_gs_ro.png")
        self.tileset_index = -1
        self.bdf_index, tileset = get_bdf_index_and_tileset("spleen-32x64.bdf")
        self.context = tcod.context.new(rows=rows, columns=cols, tileset=tileset, title=Config.default_game_name)
        self.root_console = self.context.new_console(min_rows=rows, min_columns=cols)

    def __enter__(self) -> IoWrapper:
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.context.close()

    def new_window(self, dimensions: Dimensions) -> IoWindow:
        rows, cols = dimensions.params
        new_console = self.context.new_console(min_rows=rows, min_columns=cols)
        return TcodWindow(new_console, self.root_console)

    def flush(self) -> None:
        self.context.present(self.root_console)

    def suspend(self) -> None:
        """SDL version doesn't require suspend."""
        pass

    def resume(self) -> None:
        """SDL version doesn't require resume."""
        pass

    def toggle_fullscreen(self) -> None:
        """Toggle a context window between fullscreen and windowed modes."""
        if not self.context.sdl_window_p:
            return
        fullscreen = tcod.lib.SDL_GetWindowFlags(self.context.sdl_window_p) & (
                    tcod.lib.SDL_WINDOW_FULLSCREEN | tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP
        )
        tcod.lib.SDL_SetWindowFullscreen(self.context.sdl_window_p,
                                         0 if fullscreen else tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP, )

    def next_tileset(self) -> str:
        self.tileset_index += 1
        tileset_name, tileset = get_tileset_by_index(self.tileset_index)
        self.context.change_tileset(tileset)
        self.flush()
        return tileset_name

    def previous_tileset(self) -> str:
        self.tileset_index -= 1
        tileset_name, tileset = get_tileset_by_index(self.tileset_index)
        self.context.change_tileset(tileset)
        self.flush()
        return tileset_name

    def next_bdf(self) -> str:
        self.bdf_index += 1
        tileset_name, tileset = get_bdf_tileset_by_index(self.bdf_index)
        self.context.change_tileset(tileset)
        self.flush()
        return tileset_name

    def previous_bdf(self) -> str:
        self.bdf_index -= 1
        tileset_name, tileset = get_bdf_tileset_by_index(self.bdf_index)
        self.context.change_tileset(tileset)
        self.flush()
        return tileset_name
