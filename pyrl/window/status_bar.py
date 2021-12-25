from __future__ import annotations

import textwrap
from collections.abc import Callable
from functools import wraps
from typing import Any

from pyrl.window.base_window import BaseWindow

Getter = Callable[[], Any]

class StatusBar(BaseWindow):

    """Handles the status bar system."""

    @wraps(BaseWindow.__init__, assigned=())
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        BaseWindow.__init__(self, *args, **kwargs)

        self.elements: list[tuple[str, Getter]] = []
        self.wrapper = textwrap.TextWrapper(width=self.cols)

    def update(self) -> None:
        self.clear()
        self.print_elements()
        self.blit()

    def add_element(self, string: str, getter: Getter) -> None:
        self.elements.append((string, getter))

    def print_elements(self) -> None:
        status_string = "  ".join(
            f"{string}:{getter()}" for string, getter in self.elements
        )
        lines = self.wrapper.wrap(status_string)
        for i, line in enumerate(lines):
            self.draw_str(line, (i, 0))
