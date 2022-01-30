from __future__ import annotations

import time
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import ClassVar

from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.helper_mixins import DimensionsMixin
from pyrl.structures.position import Position
from pyrl.types.char import Glyph
from pyrl.types.color import Colors, ColorPair
from pyrl.types.color_str import ColorStr
from pyrl.types.coord import Coord
from pyrl.types.keys import Keys, Key, KeyTuple

@dataclass(eq=False)
class BaseWindow(DimensionsMixin):

    # Seconds to sleep until next user input check in half-block functions
    half_block_input_responsiveness: ClassVar[float] = 0.001

    wrapper:         IoWrapper = field(repr=False)
    dimensions:      Dimensions
    screen_position: Position
    io_win:          IoWindow = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.io_win = self.wrapper.new_window(self.dimensions)

    def draw_char(self, char: Glyph, coord: Coord) -> None:
        self.io_win.draw_char(char, coord)

    def draw_str(self, string: str, coord: Coord, color: ColorPair = Colors.Normal) -> None:
        self.io_win.draw_str(string, coord, color)

    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        self.io_win.draw(glyph_info_iterable)

    def draw_reverse(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        self.io_win.draw_reverse(glyph_info_iterable)

    def clear(self) -> None:
        self.io_win.clear()

    @classmethod
    def get_time(cls) -> float:
        """Get a time in fractional seconds that is compatible with self.check_key(until=timestamp)."""
        return time.perf_counter()

    def get_key(self, keys: KeyTuple = (), refresh: bool = False) -> Key:
        """
        Return key from user.

        If keys is given only those keys are considered valid return values. Continues blocking
        until a valid key is returned by user in this case.
        """
        if refresh:
            self.refresh()

        while True:
            key = self.io_win.get_key()
            if not keys or key in keys:
                return key

    def check_key(self, keys: KeyTuple | None = None, until: float | None = None, refresh: bool = False) -> Key:
        """
        Return key if user has given one, otherwise return Key.NO_INPUT.

        If keys is given only considers those keys valid return values returning Key.NO_INPUT
        otherwise.
        If until is given doesn't immediately return on no input. Instead waits for user input until
        given time and returns Key.NO_INPUT in case no input is given in this time period.
        """
        if refresh:
            self.refresh()

        while True:
            key = self.io_win.check_key()
            if until is None or self.get_time() >= until \
                    or keys and key in keys:
                break
            time.sleep(self.half_block_input_responsiveness)

        if not keys or key in keys:
            return key
        else:
            return Keys.NO_INPUT

    def blit(self) -> None:
        self.io_win.blit(self.dimensions, self.screen_position)

    def refresh(self) -> None:
        self.blit()
        self.wrapper.flush()

    def menu(self, header: str, lines: Iterable[ColorStr], footer: str, keys: KeyTuple) -> Key:
        self.clear()
        self.draw_banner(header)
        self.draw_lines(lines, y_offset=2)
        self.draw_banner(footer, y_offset=-1)
        return self.get_key(keys=keys, refresh=True)

    def draw_lines(self, color_lines: Iterable[ColorStr], y_offset: int = 0, x_offset: int = 0) -> None:
        for i, (line, color) in enumerate(color_lines):
            self.draw_str(line, (i + y_offset, x_offset), color)

    def draw_banner(self, banner_content: str, y_offset: int = 0, color: ColorPair = Colors.Brown) -> None:
        space_padded = f"  {banner_content}  "
        full_banner = f"{space_padded:+^{self.cols}}"
        if y_offset < 0:
            self.draw_str(full_banner, (self.rows + y_offset, 0), color)
        else:
            self.draw_str(full_banner, (y_offset, 0), color)

    def get_str(self, ask_line: str = "", coord: Coord = (0, 0)) -> str:
        self.draw_str(ask_line, coord)
        input_y = coord[0]
        input_x = coord[1] + len(ask_line)
        input_coord = input_y, input_x
        user_input = ""
        cursor_index = len(user_input)
        max_input_size = self.cols - input_x - 1
        while True:
            # Normalize input
            user_input = user_input[:max_input_size]
            cursor_index = max(min(cursor_index, len(user_input)), 0)

            # Update vars
            cursor_coord = input_y, input_x + cursor_index
            cursor_char = ((user_input + " ")[cursor_index], Colors.Cursor)

            # Print
            self.draw_str(user_input, input_coord)
            self.draw_char(cursor_char, cursor_coord)
            key = self.get_key(refresh=True)
            self.draw_str(" " * (len(user_input)), input_coord)
            self.draw_char((" ", Colors.Normal), cursor_coord)

            if key == Keys.SPACE:
                key = " "

            if key in (Keys.ENTER, "^m", "^j", "^d"):
                return user_input
            elif key == "^w":
                state_whitespace = True
                del_amount = 0
                for char in reversed(user_input[:cursor_index]):
                    if state_whitespace and not char.isspace():
                        state_whitespace = False
                    elif not state_whitespace and char.isspace():
                        break
                    del_amount += 1
                user_input = user_input[:cursor_index - del_amount] + user_input[cursor_index:]
                cursor_index -= del_amount
            elif key == "^u":
                user_input = user_input[cursor_index:]
                cursor_index = 0
            elif key in (Keys.END, "^e"):
                cursor_index = len(user_input)
            elif key in (Keys.HOME, "^a"):
                cursor_index = 0
            elif key in (Keys.BACKSPACE, "^h"):
                user_input = user_input[:max(cursor_index - 1, 0)] + user_input[cursor_index:]
                cursor_index -= 1
            elif key == Keys.DELETE:
                user_input = user_input[:cursor_index] + user_input[cursor_index + 1:]
            elif key == Keys.LEFT:
                cursor_index -= 1
            elif key == Keys.RIGHT:
                cursor_index += 1
            else:
                user_input = user_input[:cursor_index] + key + user_input[cursor_index:]
                cursor_index += len(key)
