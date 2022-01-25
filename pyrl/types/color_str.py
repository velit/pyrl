from typing import Iterable

from pyrl.types.color import ColorPair, ColorPairs

ColorStr = tuple[str, ColorPair]

def from_seq(display_strings: Iterable[str], color: ColorPair = ColorPairs.Normal) -> list[ColorStr]:
    return [(display, color) for display in display_strings]
