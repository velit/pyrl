from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar

import tcod
from tcod import Console
from tcod.context import Context

from pyrl.config.config import Config
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.io_wrappers.tcod import IMPLEMENTATION
from pyrl.io_wrappers.tcod.tcod_tilesets import get_tileset_by_index, get_bdf_index_and_tileset, \
    get_bdf_tileset_by_index
from pyrl.io_wrappers.tcod.tcod_window import TcodWindow
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.helper_mixins import DimensionsMixin
from pyrl.window.window_system import WindowSystem

@dataclass
class TcodWrapper(IoWrapper, DimensionsMixin):
    """Wrapper for the chronicles of doryen roguelike library (SDL)."""

    implementation: ClassVar[str] = IMPLEMENTATION

    dimensions:    Dimensions = WindowSystem.game_dimensions
    tileset_index: int        = field(init=False)
    bdf_index:     int        = field(init=False)
    context:       Context    = field(init=False, repr=False)
    root_console:  Console    = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Init the SDL surface and prepare for draw calls."""
        # self.tileset_index, tileset = get_index_and_tileset("terminal10x18_gs_ro.png")
        self.tileset_index = 0
        self.bdf_index, tileset = get_bdf_index_and_tileset("spleen-16x32.bdf")
        self.context = tcod.context.new(width=1536, height=960, tileset=tileset, title=Config.default_game_name)
                                        # sdl_window_flags=(tcod.context.SDL_WINDOW_MAXIMIZED |
                                        #                   tcod.context.SDL_WINDOW_RESIZABLE))
        self.root_console = self.context.new_console(min_rows=self.rows, min_columns=self.cols)

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
