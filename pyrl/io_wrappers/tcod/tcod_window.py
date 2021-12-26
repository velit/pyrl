from __future__ import annotations

from typing import Iterable

import tcod

from tests.integration_tests.dummy_plug_system import handle_dummy_input
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.tcod import IMPLEMENTATION
from pyrl.io_wrappers.tcod.tcod_colors import tcod_color_map
from pyrl.io_wrappers.tcod.tcod_keys import tcod_key_map
from pyrl.types.char import Glyph
from pyrl.types.color import Color, ColorPair, ColorPairs
from pyrl.types.coord import Coord
from pyrl.types.keys import Keys, Key

class TcodWindow(IoWindow):
    implementation = IMPLEMENTATION
    key_map = tcod_key_map
    color_map = tcod_color_map

    def __init__(self, libtcod_console: tcod.Console) -> None:
        self.default_fg = self.color_map[Color.Normal]
        self.default_bg = self.color_map[Color.Black]
        self.console: tcod.Console = libtcod_console
        tcod.console_set_default_foreground(self.console, self.default_fg)
        tcod.console_set_default_background(self.console, self.default_bg)

    @handle_dummy_input
    def get_key(self) -> Key:
        while True:
            key_event = tcod.Key()
            mouse_event = tcod.Mouse()
            tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key_event, mouse_event, False)
            key = self._interpret_event(key_event)
            if key != Keys.NO_INPUT:
                return key

    def check_key(self) -> Key:
        event = tcod.console_check_for_keypress(tcod.KEY_PRESSED)
        return self._interpret_event(event)

    def _interpret_event(self, event: tcod.Key) -> Key:
        if tcod.console_is_window_closed():
            return Keys.CLOSE_WINDOW
        elif event.vk in self.key_map:
            return self.key_map[event.vk]
        elif event.vk == tcod.KEY_CHAR:
            if event.c == ord('c') and event.lctrl or event.rctrl:
                raise KeyboardInterrupt
            ch = chr(event.c)
            if event.shift:
                ch = ch.upper()
            if event.lctrl or event.rctrl:
                ch = "^" + ch
            if event.lalt or event.ralt:
                ch = "!" + ch
            return ch
        else:
            return Keys.NO_INPUT

    def clear(self) -> None:
        tcod.console_clear(self.console)

    def blit(self, size: tuple[int, int], screen_position: tuple[int, int]) -> None:
        rows, cols = size
        y, x = screen_position
        tcod.console_blit(self.console, 0, 0, cols, rows, 0, x, y, 1.0, 1.0)

    def get_dimensions(self) -> tuple[int, int]:
        return tcod.console_get_height(self.console), tcod.console_get_width(self.console)

    def draw_char(self, char: Glyph, coord: Coord) -> None:
        y, x = coord
        symbol, (fg, bg) = char
        tcod.console_put_char_ex(self.console, x, y, symbol, self.color_map[fg], self.color_map[bg])

    def draw_str(self, string: str, coord: Coord, color: ColorPair | None = None) -> None:
        y, x = coord
        if color is None:
            fg, bg = ColorPairs.Normal
        else:
            fg, bg = color
        tcod.console_set_color_control(tcod.COLCTRL_1, self.color_map[fg], self.color_map[bg])
        string = chr(tcod.COLCTRL_1) + string + chr(tcod.COLCTRL_STOP)
        tcod.console_print(self.console, x, y, string)

    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        _draw = tcod.console_put_char_ex
        local_color = self.color_map
        for (y, x), (symbol, (fg, bg)) in glyph_info_iterable:
            _draw(self.console, x, y, symbol, local_color[fg], local_color[bg])

    def draw_reverse(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        _draw = tcod.console_put_char_ex
        local_color = self.color_map
        for (y, x), (symbol, (fg, bg)) in glyph_info_iterable:
            _draw(self.console, x, y, symbol, local_color[bg], local_color[fg])
