from __future__ import annotations

import curses
import curses.ascii
import logging
from _curses import _CursesWindow
from typing import Iterable

from pyrl.config.debug import Debug
from pyrl.types.char import Glyph
from pyrl.types.color import ColorPair
from pyrl.types.coord import Coord
from pyrl.types.keys import Keys
from pyrl.io_wrappers.curses import IMPLEMENTATION, WideChar
from pyrl.io_wrappers.curses.curses_dicts import Curses256ColorDict, CursesColorDict
from pyrl.io_wrappers.curses.curses_keys import curses_key_map
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.window.window_system import WindowSystem

class CursesWindow(IoWindow):

    implementation = IMPLEMENTATION
    color_map: dict[ColorPair, int]
    key_map: dict[WideChar, str] = curses_key_map

    def __init__(self, curses_window: _CursesWindow, root_window: CursesWindow | None = None) -> None:
        if root_window is None:
            self.root_win = self
        else:
            self.root_win = root_window
        if not hasattr(CursesWindow, "color_map"):
            if curses.COLORS == 256:
                CursesWindow.color_map = Curses256ColorDict()
            else:
                CursesWindow.color_map = CursesColorDict()

        self.win = curses_window
        self.win.keypad(True)
        self.win.immedok(False)
        self.win.scrollok(False)

    def get_key(self) -> str:
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

    def check_key(self) -> str:
        """Non-blocking version of get_key."""
        self.win.nodelay(True)
        try:
            return self._get_key_unguarded()
        except curses.error as err:
            if err.args == ("no input", ):
                return Keys.NO_INPUT
            else:
                raise
        finally:
            self.win.nodelay(False)

    def clear(self) -> None:
        self.win.erase()

    def blit(self, size: tuple[int, int], screen_position: tuple[int, int]) -> None:
        self._ensure_terminal_is_big_enough()
        rows, cols = size
        y, x = screen_position
        self.win.noutrefresh(0, 0, y, x, y + rows - 1, x + cols - 1)

    def get_dimensions(self) -> tuple[int, int]:
        return self.win.getmaxyx()

    def draw_char(self, char: Glyph, coord: Coord) -> None:
        y, x = coord
        symbol, color = char
        self.win.addstr(y, x, symbol, self.color_map[color])

    def draw_str(self, string: str, coord: Coord, color: ColorPair | None = None) -> None:
        y, x = coord
        if color is None:
            self.win.addstr(y, x, string)
        else:
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

    def _interpret_ch(self, key: WideChar, alt: bool) -> str:

        if Debug.show_keycodes and key != Keys.NO_INPUT:
            raw = key

        if key == curses.KEY_RESIZE:
            self._ensure_terminal_is_big_enough()

        if key in self.key_map:
            key = self.key_map[key]
        elif isinstance(key, int):
            key = str(key)
        else:
            nr = ord(key)
            if nr < 128:
                key = alt * "!" + curses.ascii.unctrl(key)
                if "^" in key:
                    key = key.lower()
            else:
                key = alt * "!" + key

        if Debug.show_keycodes and key != Keys.NO_INPUT:
            logging.debug(f"User input: raw: {raw} interp: {key}{' alt:yes' * alt}")

        return key

    def _handle_alt(self, key: WideChar) -> tuple[WideChar, bool]:
        alt = False
        if key == chr(curses.ascii.ESC):
            second_key = self.check_key()
            if second_key != Keys.NO_INPUT:
                key = second_key
                alt = True
        return key, alt

    def _ensure_terminal_is_big_enough(self) -> None:
        rows, cols = self.root_win.get_dimensions()
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
                    exit()
            self.root_win.clear()
            self.root_win.win.refresh()
            rows, cols = self.root_win.get_dimensions()
