from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, Iterable, ClassVar

from pyrl.structures.dimensions import Dimensions
from pyrl.structures.position import Position
from pyrl.types.glyphs import ColorPair, Glyph
from pyrl.types.directions import Coord

class IoWindow(Protocol):
    implementation: ClassVar[str]

    @property
    def dimensions(self) -> Dimensions:
        raise NotImplementedError

    @abstractmethod
    def get_key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def check_key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def blit(self, size: Dimensions, screen_position: Position) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw_glyph(self, glyph: Glyph, coord: Coord) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw_str(self, string: str, coord: Coord, color: ColorPair) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw_reverse(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        raise NotImplementedError
