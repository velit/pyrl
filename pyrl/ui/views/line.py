from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pyrl.engine.enums.glyphs import ColorPair, Colors, ColorStr

@dataclass(order=True, frozen=True)
class Line[T]:
    """line_view Line"""
    display: str
    return_value: T
    color: ColorPair = Colors.Normal

def from_iter(display_strings: Iterable[str], color: ColorPair = Colors.Normal) -> list[ColorStr]:
    return [(display, color) for display in display_strings]

def from_multiline_str(multi_line_str: str, color: ColorPair = Colors.Normal) -> list[ColorStr]:
    return [(display, color) for display in multi_line_str.splitlines()]
