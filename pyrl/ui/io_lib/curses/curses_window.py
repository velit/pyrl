from __future__ import annotations

import curses
import curses.ascii
import logging
import sys
from typing import Iterable, TYPE_CHECKING, ClassVar

assert sys.platform != "win32"

from pyrl.config.debug import Debug
from pyrl.engine.structures.dimensions import Dimensions
from pyrl.engine.structures.position import Position
from pyrl.engine.types.directions import Coord
from pyrl.engine.types.glyphs import ColorPair, Colors, Glyph
from pyrl.engine.types.keys import Key, AnyKey
from pyrl.ui.io_lib.curses import IMPLEMENTATION, WideChar
from pyrl.ui.io_lib.curses.curses_dicts import Curses256ColorDict, CursesColorDict
from pyrl.ui.io_lib.curses.curses_keys import curses_key_map
from pyrl.ui.io_lib.protocol.io_window import IoWindow
from pyrl.ui.window.window_system import WindowSystem
from tests.integration_tests.dummy_plug_system import handle_dummy_input

if TYPE_CHECKING:
    from _curses import _CursesWindow

class CursesWindow(IoWindow):

    implementation: ClassVar[str] = IMPLEMENTATION
    color_map: ClassVar[dict[ColorPair, int]]
    key_map: ClassVar[dict[WideChar, str]] = curses_key_map

    win: _CursesWindow
    root_win: CursesWindow

    def __init__(self, curses_window: _CursesWindow, root_window: CursesWindow | None = None) -> None:
        self.win = curses_window
        if root_window is None:
            self.root_win = self
        else:
            self.root_win = root_window
        if not hasattr(CursesWindow, "color_map"):
            if curses.COLORS == 256:
                CursesWindow.color_map = Curses256ColorDict()
            else:
                CursesWindow.color_map = CursesColorDict()
        self.win.keypad(True)
        self.win.immedok(False)
        self.win.scrollok(False)

    @property
    def dimensions(self) -> Dimensions:
        return Dimensions(*self.win.getmaxyx())

    @handle_dummy_input
    def get_key(self) -> AnyKey:
        ch = ""
        while True:
            try:
                ch = self.win.get_wch()
                break
            except curses.error as err:
                if err.args == ("no input", ):
                    continue
                else:
                    raise
        return self._interpret_ch(*self._handle_alt(ch))

    def check_key(self) -> AnyKey:
        """Non-blocking version of get_key."""
        self.win.nodelay(True)
        try:
            return self._get_key_unguarded()
        except curses.error as err:
            if err.args == ("no input", ):
                return Key.NO_INPUT
            else:
                raise
        finally:
            self.win.nodelay(False)

    def clear(self) -> None:
        self.win.erase()

    def blit(self, size: Dimensions, screen_position: Position) -> None:
        self._ensure_terminal_is_big_enough()
        rows, cols = size.params
        y, x = screen_position
        self.win.noutrefresh(0, 0, y, x, y + rows - 1, x + cols - 1)

    def draw_glyph(self, glyph: Glyph, coord: Coord) -> None:
        y, x = coord
        symbol, color = glyph
        self.win.addstr(y, x, symbol, self.color_map[color])

    def draw_str(self, string: str, coord: Coord, color: ColorPair = Colors.Normal) -> None:
        y, x = coord
        self.win.addstr(y, x, string, self.color_map[color])

    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        local_addch = self.win.addstr
        local_color = self.color_map
        for (y, x), (symbol, color) in glyph_info_iterable:
            local_addch(y, x, symbol, local_color[color])

    def draw_reverse(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        local_addch = self.win.addstr
        local_color = self.color_map
        for (y, x), (symbol, (fg, bg)) in glyph_info_iterable:
            local_addch(y, x, symbol, local_color[bg, fg])

    def _move(self, y: int, x: int) -> None:
        self.win.move(y, x)

    def _get_cursor_pos(self) -> Coord:
        return self.win.getyx()

    def _get_key_unguarded(self) -> str:
        return self._interpret_ch(*self._handle_alt(self.win.get_wch()))

    def _interpret_ch(self, raw: WideChar, alt: bool) -> str:
        if raw == curses.KEY_RESIZE:
            self._ensure_terminal_is_big_enough()

        if raw in self.key_map:
            key = self.key_map[raw]
        elif isinstance(raw, int):
            key = str(raw)
        else:
            if ord(raw) < 128:
                key = alt * "!" + curses.ascii.unctrl(raw)
                if "^" in key:
                    key = key.lower()
            else:
                key = alt * "!" + raw

        if Debug.show_keycodes and raw != Key.NO_INPUT:
            logging.debug(f"User input: raw: {raw} interp: {key}{' alt:yes' * alt}")

        return key

    def _handle_alt(self, key: WideChar) -> tuple[WideChar, bool]:
        alt = False
        if key == chr(curses.ascii.ESC):
            second_key = self.check_key()
            if second_key != Key.NO_INPUT:
                key = second_key
                alt = True
        return key, alt

    def _ensure_terminal_is_big_enough(self) -> None:
        rows, cols = self.root_win.dimensions.params
        min_rows, min_cols = WindowSystem.game_dimensions.params
        while rows < min_rows or cols < min_cols:
            message = (f"Game needs at least a screen size of {min_cols}x{min_rows} while the "
                       f"current size is {cols}x{rows}. Please resize the screen or press Q to quit.")
            self.root_win.draw_str(message, (0, 0))
            self.root_win.win.refresh()

            if self.root_win.get_key() == "Q":
                self.root_win.clear()
                message = "Confirm quit by pressing Y."
                self.root_win.draw_str(message, (0, 0))
                self.root_win.win.refresh()
                if self.root_win.get_key() == "Y":
                    sys.exit(0)
            self.root_win.clear()
            self.root_win.win.refresh()
            rows, cols = self.root_win.dimensions.params
