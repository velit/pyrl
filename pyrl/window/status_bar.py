from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from textwrap import TextWrapper
from typing import Any

from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.position import Position
from pyrl.window.base_window import BaseWindow

Getter = Callable[[], Any]

@dataclass(eq=False)
class StatusBar(BaseWindow):
    """Handles the status bar system."""

    elements: list[tuple[str, Getter]] = field(repr=False, default_factory=list)
    text_wrapper: TextWrapper          = field(init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.text_wrapper = TextWrapper(width=self.cols)

    def update(self) -> None:
        self.clear()
        self.print_elements()
        self.blit()

    def add_element(self, element: Any, getter: Getter) -> None:
        self.elements.append((element, getter))

    def print_elements(self) -> None:
        status_string = "  ".join(
            f"{string}:{getter()}" for string, getter in self.elements
        )
        lines = self.text_wrapper.wrap(status_string)
        for i, line in enumerate(lines):
            self.draw_str(line, (i, 0))
