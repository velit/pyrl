from __future__ import annotations

from typing import Iterable

from pyrl.game_data.levels.shared_assets import default_dims
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.position import Position
from tests.integration_tests.dummy_plug_system import handle_dummy_input
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.mock import IMPLEMENTATION
from pyrl.types.char import Glyph
from pyrl.types.color import ColorPair
from pyrl.types.coord import Coord
from pyrl.types.keys import Keys, Key

class MockWindow(IoWindow):

    implementation = IMPLEMENTATION

    def __init__(self) -> None:
        pass

    @handle_dummy_input
    def get_key(self) -> Key:
        return Keys.NO_INPUT

    def check_key(self) -> Key:
        return Keys.NO_INPUT

    def clear(self) -> None:
        pass

    def blit(self, size: Dimensions, screen_position: Position) -> None:
        pass

    def get_dimensions(self) -> Dimensions:
        return default_dims

    def draw_char(self, char: Glyph, coord: Coord) -> None:
        pass

    def draw_str(self, string: str, coord: Coord, color: ColorPair | None = None) -> None:
        pass

    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        pass

    def draw_reverse(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        pass
