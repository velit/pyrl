from typing import Iterable

from pyrl.types.color import ColorPair, Colors

ColorStr = tuple[str, ColorPair]

def from_seq(display_strings: Iterable[str], color: ColorPair = Colors.Normal) -> list[ColorStr]:
    return [(display, color) for display in display_strings]
