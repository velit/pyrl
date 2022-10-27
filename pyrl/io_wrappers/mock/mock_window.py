from __future__ import annotations

from typing import Iterable

from pyrl.game_data.levels.shared_assets import default_dims
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.position import Position
from tests.integration_tests.dummy_plug_system import handle_dummy_input
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.mock import IMPLEMENTATION
from pyrl.types.glyphs import ColorPair, Colors, Glyph
from pyrl.types.directions import Coord
from pyrl.types.keys import Key, AnyKey

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
