from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Iterable, Any, ClassVar

import tcod
from tcod.console import Console
from tcod.event import Modifier

from pyrl.engine.structures.dimensions import Dimensions
from pyrl.engine.structures.helper_mixins import DimensionsMixin
from pyrl.engine.structures.position import Position
from pyrl.engine.types.directions import Coord
from pyrl.engine.types.glyphs import Color, ColorPair, Colors, Glyph
from pyrl.engine.types.keys import Key, AnyKey
from pyrl.ui.io_lib.protocol.io_window import IoWindow
from pyrl.ui.io_lib.tcod import IMPLEMENTATION
from pyrl.ui.io_lib.tcod.tcod_colors import color_map
from pyrl.ui.io_lib.tcod.tcod_keys import key_map, ignore_keys
from tests.integration_tests.dummy_plug_system import handle_dummy_input

@dataclass
class TcodWindow(IoWindow, DimensionsMixin):
    implementation: ClassVar[str] = IMPLEMENTATION

    console: Console = field(repr=False)
    root_console: Console = field(repr=False)

    @property
    def dimensions(self) -> Dimensions:
        return Dimensions(self.console.height, self.console.width)

    @handle_dummy_input
    def get_key(self) -> AnyKey:
        while (key := self._interpret_events(tcod.event.wait())) == Key.NO_INPUT:
            pass
        return key

    def check_key(self) -> AnyKey:
        return self._interpret_events(tcod.event.get())

    def _interpret_events(self, events: Iterator[Any]) -> AnyKey:
        for event in events:
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()
            # elif isinstance(event, tcod.event.WindowResized):
            #     return Keys.WINDOW_RESIZE
            elif isinstance(event, tcod.event.KeyDown):
                if event.sym in key_map:
                    return key_map[event.sym]
                if event.sym in ignore_keys:
                    continue
                key = event.sym.label
                if event.mod & Modifier.SHIFT:
                    key = key.upper()
                else:
                    key = key.lower()
                if event.mod & Modifier.LGUI or event.mod & Modifier.RGUI:
                    key = "◆" + key
                if event.mod & Modifier.CTRL:
                    key = "^" + key
                if event.mod & Modifier.ALT:
                    key = "!" + key
                if key == "^c":
                    raise KeyboardInterrupt
                return key
        return Key.NO_INPUT

    def clear(self) -> None:
        self.console.clear(fg=color_map[Color.Normal], bg=color_map[Color.Black])

    def blit(self, size: Dimensions, screen_position: Position) -> None:
        y, x = screen_position
        self.console.blit(self.root_console, dest_y=y, dest_x=x, width=size.cols, height=size.rows)

    def draw_glyph(self, glyph: Glyph, coord: Coord) -> None:
        y, x = coord
        symbol, (fg, bg) = glyph
        self.console.print(y=y, x=x, string=symbol, fg=color_map[fg], bg=color_map[bg])

    def draw_str(self, string: str, coord: Coord, color: ColorPair = Colors.Normal) -> None:
        y, x = coord
        fg_colo, bg_colo = color
        fg, bg = color_map[fg_colo], color_map[bg_colo]
        self.console.print(y=y, x=x, string=string, fg=fg, bg=bg)

    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        _print = self.console.print
        for (y, x), (symbol, (fg, bg)) in glyph_info_iterable:
            _print(y=y, x=x, string=symbol, fg=color_map[fg], bg=color_map[bg])

    def draw_reverse(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        _print = self.console.print
        for (y, x), (symbol, (fg, bg)) in glyph_info_iterable:
            _print(y=y, x=x, string=symbol, fg=color_map[bg], bg=color_map[fg])
