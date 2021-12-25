from __future__ import annotations

import logging
from typing import Iterable, TYPE_CHECKING

from pyrl.game_data.levels.shared_assets import default_dims
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.mock import IMPLEMENTATION
from pyrl.types.char import Glyph
from pyrl.types.color import ColorPair
from pyrl.types.coord import Coord
from pyrl.types.keys import Keys

if TYPE_CHECKING:
    from pyrl.io_wrappers.mock.mock_wrapper import MockWrapper

class MockWindow(IoWindow):

    implementation = IMPLEMENTATION

    def __init__(self, mockwrapper: MockWrapper):
        self.wrapper = mockwrapper

    def get_key(self) -> str:
        try:
            key = self.wrapper._prepared_input.popleft()
            logging.debug(f"Returning key {key}")
            return key
        except IndexError:
            from pyrl.io_wrappers.mock.mock_wrapper import MockInputEnd
            raise MockInputEnd()

    def check_key(self) -> str:
        return Keys.NO_INPUT

    def clear(self) -> None:
        pass

    def blit(self, size: tuple[int, int], screen_position: tuple[int, int]) -> None:
        pass

    def get_dimensions(self) -> tuple[int, int]:
        return default_dims.params

    def draw_char(self, char: Glyph, coord: Coord) -> None:
        pass

    def draw_str(self, string: str, coord: Coord, color: ColorPair | None = None) -> None:
        pass

    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        pass

    def draw_reverse(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        pass
