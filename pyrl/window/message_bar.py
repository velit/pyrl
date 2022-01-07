from __future__ import annotations

import logging
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from textwrap import TextWrapper
from typing import Any

from pyrl.config.binds import Binds
from pyrl.io_wrappers import mock
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.structures.dimensions import Dimensions
from pyrl.structures.position import Position
from pyrl.types.color import ColorPairs
from pyrl.window.base_window import BaseWindow

MORE_STR = " More"
MORE_STR_LEN = len(MORE_STR)

@dataclass(init=False, eq=False)
class MessageBar(BaseWindow):
    """Handles the messaging bar system."""

    history: list[str]
    msgqueue: list[str]
    wrap: Callable[[str], list[str]]

    def __init__(self, wrapper: IoWrapper, dimensions: Dimensions, screen_position: Position) -> None:
        super().__init__(wrapper, dimensions, screen_position)

        self.history = []
        self.msgqueue = []
        self.wrap = TextWrapper(width=(self.cols - MORE_STR_LEN)).wrap

    def update(self) -> None:
        self.clear()
        if self.msgqueue:
            self.print_event(self.msgqueue)
            self.add_lines_to_history(self.msgqueue)
            self.msgqueue = []
        self.blit()

    def debug_msg(self, obj: Any) -> None:
        logging.debug(f"io.msg: {obj}")

    def queue_msg(self, *args: Any) -> None:
        output: Callable[[str], Any]
        if self.io_win.implementation == mock.IMPLEMENTATION:
            output = self.debug_msg
        else:
            output = self.msgqueue.append
        for obj in args:
            output(str(obj))

    def add_lines_to_history(self, lines: Iterable[str]) -> None:
        for msg in lines:
            lastitem = self.history[-1] if self.history else ""

            if msg == lastitem:
                self.history[-1] = f"{msg} (x2)"
                continue

            if msg == lastitem[:len(msg)]:
                result = re.match(r" \(x(\d+)\)", lastitem[len(msg):])
                if result:
                    repeat_number = int(result.group(1)) + 1
                    self.history[-1] = f"{msg} (x{repeat_number})"
                    continue

            self.history.append(msg)

    def print_event(self, event: Iterable[str]) -> None:
        skip = False
        lines = self.wrap(" ".join(event))
        for i, line in enumerate(lines):
            self.draw_str(line, (i % self.rows, 0))
            if i % self.rows == self.rows - 1 and i != len(lines) - 1:
                self.draw_str(MORE_STR, (self.rows - 1, self.cols - MORE_STR_LEN), ColorPairs.Green)
                key = self.get_key(keys=Binds.Skip_To_Last_Message + Binds.Cancel, refresh=True)
                if key in Binds.Skip_To_Last_Message:
                    skip = True
                    break
                self.clear()
        if skip:
            self.clear()
            for i in range(self.rows):
                self.draw_str(lines[i - self.rows], (i, 0))
