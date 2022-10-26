from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any, ClassVar

from pyrl.config.config import Config
from pyrl.config.debug import Debug
from pyrl.game_data.levels.shared_assets import default_dims
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.position import Position
from pyrl.types.glyph import Glyph
from pyrl.types.color import Colors, ColorPair
from pyrl.types.color_str import ColorStr
from pyrl.types.coord import Coord
from pyrl.types.keys import Key, KeyTuple
from pyrl.types.line import Line
from pyrl.window.base_window import BaseWindow
from pyrl.window.level_window import LevelWindow
from pyrl.window.message_bar import MessageBar
from pyrl.window.status_bar import StatusBar

@dataclass(eq=False)
class WindowSystem:

    message_dimensions: ClassVar[Dimensions] = Dimensions(Config.message_bar_height, default_dims.cols)
    status_dimensions: ClassVar[Dimensions] = Dimensions(Config.status_bar_height, default_dims.cols)
    game_dimensions: ClassVar[Dimensions] = Dimensions(message_dimensions.rows + status_dimensions.rows +
                                                       default_dims.rows, default_dims.cols)

    wrapper:      IoWrapper
    whole_window: BaseWindow  = field(init=False)
    message_bar:  MessageBar  = field(init=False)
    level_window: LevelWindow = field(init=False)
    status_bar:   StatusBar   = field(init=False)

    def __post_init__(self) -> None:
        self.whole_window = BaseWindow(self.wrapper, self.game_dimensions, Position(0, 0))
        self.message_bar  = MessageBar(self.wrapper, self.message_dimensions, Position(0, 0))
        self.level_window = LevelWindow(self.wrapper, default_dims,
                                        Position(self.message_bar.screen_position.y + self.message_bar.rows, 0))
        self.status_bar   = StatusBar(self.wrapper, self.status_dimensions,
                                      Position(self.level_window.screen_position.y + self.level_window.rows, 0))

    def get_key(self, message: str | None = None, keys: KeyTuple = ()) -> Key:
        if message:
            self.msg(message)
        self.refresh()
        return self.whole_window.get_key(keys=keys)

    def check_key(self, message: str | None = None, keys: KeyTuple | None = None, until: float | None = None) -> Key:
        if message:
            self.msg(message)
        self.refresh()
        return self.whole_window.check_key(keys=keys, until=until)

    def msg(self, *messages: Any, color: ColorPair = Colors.Normal) -> None:
        self.message_bar.queue_msg(*messages, color=color)

    def refresh(self) -> None:
        self.message_bar.update()
        self.level_window.update()
        self.status_bar.update()
        self.wrapper.flush()

    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]], reverse: bool = False) -> None:
        if not reverse:
            self.level_window.draw(glyph_info_iterable)
        else:
            self.level_window.draw_reverse(glyph_info_iterable)

    def menu(self, header: str, lines: Iterable[ColorStr], footer: str, keys: KeyTuple) -> Key:
        return self.whole_window.menu(header, lines, footer, keys)

    def draw_glyph(self, glyph: Glyph, coord: Coord, reverse: bool = False) -> None:
        self.level_window.draw_glyph(glyph, coord, reverse)

    def draw_line(self, a: Coord, b: Coord, glyph: Glyph = ('*', Colors.Yellow), draw_first: bool = False) -> None:
        self.level_window.draw_line(a, b, glyph, draw_first)

    def draw_path(self, path: Iterable[Coord]) -> None:
        for coord in path:
            self.draw_glyph((" ", Colors.Green), coord, reverse=True)
            if Debug.path_step:
                self.level_window.get_key(refresh=True)
        if not Debug.path_step:
            self.level_window.get_key(refresh=True)

    def suspend(self) -> None:
        self.wrapper.suspend()

    def resume(self) -> None:
        self.wrapper.resume()

    def get_str(self, ask_line: str = "", coord: Coord = (0, 0)) -> str:
        self.message_bar.clear()
        return self.message_bar.get_str(ask_line=ask_line, coord=coord)

    def get_future_time(self, delay: float) -> float:
        return BaseWindow.get_time() + delay

    def get_time(self) -> float:
        return BaseWindow.get_time()
