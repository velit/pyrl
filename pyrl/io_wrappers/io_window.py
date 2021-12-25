from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, Iterable

from pyrl.types.char import Glyph
from pyrl.types.color import ColorPair
from pyrl.types.coord import Coord

class IoWindow(Protocol):
    implementation: str

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
    def blit(self, size: tuple[int, int], screen_position: tuple[int, int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_dimensions(self) -> tuple[int, int]:
        raise NotImplementedError

    @abstractmethod
    def draw_char(self, char: Glyph, coord: Coord) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw_str(self, string: str, coord: Coord, color: ColorPair | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw_reverse(self, glyph_info_iterable: Iterable[tuple[Coord, Glyph]]) -> None:
        raise NotImplementedError
