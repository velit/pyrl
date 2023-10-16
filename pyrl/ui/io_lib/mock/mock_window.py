from __future__ import annotations

from typing import Iterable

from pyrl.engine.structures.dimensions import Dimensions
from pyrl.engine.structures.position import Position
from pyrl.engine.enums.directions import Coord
from pyrl.engine.enums.glyphs import ColorPair, Colors, Glyph
from pyrl.engine.enums.keys import Key, AnyKey
from pyrl.game_data.levels.shared_assets import default_dims
from pyrl.ui.io_lib.mock import IMPLEMENTATION
from pyrl.ui.io_lib.protocol.io_window import IoWindow
from tests.integration_tests.dummy_plug_system import handle_dummy_input

class MockWindow(IoWindow):

    implementation = IMPLEMENTATION

    def __init__(self) -> None:
        return

    @property
    def dimensions(self) -> Dimensions:
        return default_dims

    @handle_dummy_input
    def get_key(self) -> AnyKey:
        return Key.NO_INPUT

    def check_key(self) -> AnyKey:
        return Key.NO_INPUT

    def clear(self) -> None:
        return

    def blit(self, size: Dimensions, screen_position: Position) -> None:
        return

    def draw_glyph(self, glyph: Glyph, coord: Coord) -> None:
        return

    def draw_str(self, string: str, coord: Coord, color: ColorPair = Colors.Normal) -> None:
        return

    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        return

    def draw_reverse(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        return
