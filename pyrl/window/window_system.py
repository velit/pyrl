from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Sequence
from typing import Any

from pyrl.config.config import Config
from pyrl.config.debug import Debug
from pyrl.game_data.levels.shared_assets import default_dims
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.position import Position
from pyrl.types.char import Glyph
from pyrl.types.color import ColorPairs
from pyrl.types.coord import Coord
from pyrl.types.keys import Key, KeyTuple
from pyrl.window.base_window import BaseWindow
from pyrl.window.level_window import LevelWindow
from pyrl.window.message_bar import MessageBar
from pyrl.window.status_bar import StatusBar

class WindowSystem:

    message_dimensions = Dimensions(Config.message_bar_height, default_dims.cols)
    status_dimensions = Dimensions(Config.status_bar_height, default_dims.cols)
    game_dimensions = Dimensions(message_dimensions.rows + status_dimensions.rows + default_dims.rows,
                                 default_dims.cols)

    def __init__(self, cursor_lib: IoWrapper) -> None:
        self.cursor_lib = cursor_lib

        self.whole_window = BaseWindow(cursor_lib, self.game_dimensions, Position(0, 0))
        self.message_bar  = MessageBar(cursor_lib, self.message_dimensions, Position(0, 0))
        self.level_window = LevelWindow(cursor_lib, default_dims,
                                        Position(self.message_bar.screen_position.y + self.message_bar.rows, 0))
        self.status_bar   = StatusBar(cursor_lib, self.status_dimensions,
                                      Position(self.level_window.screen_position.y + self.level_window.rows, 0))

        self.prepared_input: deque[Key] = deque()

    def get_key(self, message: str | None = None, keys: KeyTuple | None = None) -> Key:
        if message:
            self.msg(message)

        self.refresh()

        if self.prepared_input:
            return self.prepared_input.popleft()

        return self.whole_window.get_key(keys=keys)

    def check_key(self, message: str | None = None, keys: KeyTuple | None = None, until: float | None = None) -> Key:
        if message:
            self.msg(message)

        self.refresh()

        return self.whole_window.check_key(keys=keys, until=until)

    def msg(self, *messages: Any) -> None:
        self.message_bar.queue_msg(*messages)

    def refresh(self) -> None:
        self.message_bar.update()
        self.level_window.update()
        self.status_bar.update()
        self.cursor_lib.flush()

    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]], reverse: bool = False) -> None:
        if not reverse:
            self.level_window.draw(glyph_info_iterable)
        else:
            self.level_window.draw_reverse(glyph_info_iterable)

    def menu(self, header: str, lines: Sequence[str], footer: str, keys: KeyTuple) -> Key:
        return self.whole_window.menu(header, lines, footer, keys)

    def draw_char(self, char: Glyph, coord: Coord, reverse: bool = False) -> None:
        self.level_window.draw_char(char, coord, reverse)

    def draw_line(self, a: Coord, b: Coord, char: Glyph = ('*', ColorPairs.Yellow), draw_first: bool = False) -> None:
        self.level_window.draw_line(a, b, char, draw_first)

    def draw_path(self, path: Iterable[Coord]) -> None:
        for coord in path:
            self.draw_char((" ", ColorPairs.Green), coord, reverse=True)
            if Debug.path_step:
                self.level_window.get_key(refresh=True)
        if not Debug.path_step:
            self.level_window.get_key(refresh=True)

    def suspend(self) -> None:
        self.cursor_lib.suspend()

    def resume(self) -> None:
        self.cursor_lib.resume()

    def get_str(self, ask_line: str = "", coord: Coord = (0, 0)) -> str:
        self.message_bar.clear()
        return self.message_bar.get_str(ask_line=ask_line, coord=coord)

    def get_future_time(self, delay: float) -> float:
        return BaseWindow.get_time() + delay

    def get_time(self) -> float:
        return BaseWindow.get_time()
