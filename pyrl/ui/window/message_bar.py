from __future__ import annotations

import logging
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from textwrap import TextWrapper
from typing import Any

from pyrl.config.binds import Binds
from pyrl.engine.types.glyphs import Colors, ColorPair
from pyrl.ui.io_lib import mock
from pyrl.ui.window.base_window import BaseWindow

MORE_STR = " More"
MORE_STR_LEN = len(MORE_STR)

@dataclass(eq=False)
class MessageBar(BaseWindow):
    """Handles the messaging bar system."""

    history: list[tuple[str, ColorPair]]  = field(init=False, repr=False, default_factory=list)
    msgqueue: list[tuple[str, ColorPair]] = field(init=False, repr=False, default_factory=list)
    text_wrapper: TextWrapper             = field(init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.text_wrapper = TextWrapper(self.cols - MORE_STR_LEN)

    def update(self) -> None:
        self.clear()
        if self.msgqueue:
            self.print_events(self.msgqueue)
            self.add_lines_to_history(self.msgqueue)
            self.msgqueue = []
        self.blit()

    def debug_msg(self, obj: Any) -> None:
        logging.debug(f"io.msg: {obj}")

    def queue_msg(self, *args: Any, color: ColorPair = Colors.Normal) -> None:
        output: Callable[[str], Any]
        for obj in args:
            if self.io_win.implementation == mock.IMPLEMENTATION:
                self.debug_msg(str(obj))
            else:
                self.msgqueue.append((str(obj), color))

    def add_lines_to_history(self, lines: Iterable[tuple[str, ColorPair]]) -> None:
        for msg, color in lines:
            if self.history:
                lastitem, lastcolor = self.history[-1]

                if msg == lastitem:
                    self.history[-1] = (f"{msg} (x2)", color)
                    continue

                if msg == lastitem[:len(msg)]:
                    result = re.match(r" \(x(\d+)\)", lastitem[len(msg):])
                    if result:
                        repeat_number = int(result.group(1)) + 1
                        self.history[-1] = (f"{msg} (x{repeat_number})", color)
                        continue

            for chunk in self.text_wrapper.wrap(msg):
                self.history.append((chunk, color))

    def print_events(self, events: Iterable[tuple[str, ColorPair]]) -> None:
        i, line = 0, 0
        skip = False
        for message, color in events:
            for chunk in self._chunkify(message):
                padding = MORE_STR_LEN if line == self.rows - 1 else 1
                if len(chunk) > self.cols - i - padding:
                    i = 0
                    line += 1
                if line >= self.rows:
                    if not skip:
                        self.draw_str(MORE_STR, (self.rows - 1, self.cols - MORE_STR_LEN), Colors.Green)
                        key = self.get_key(keys=Binds.Skip_To_Last_Message + Binds.Cancel, refresh=True)
                        if key in Binds.Skip_To_Last_Message:
                            skip = True
                    line = 0
                    self.clear()

                self.draw_str(chunk, (line, i), color)
                i += len(chunk) + 1

    def _chunkify(self, message: str) -> Iterable[str]:
        return [chunk for word in message.split() for chunk in self._splitify(word)]

    def _splitify(self, word: str) -> Iterable[str]:
        if len(word) > self.cols - MORE_STR_LEN:
            return self.text_wrapper.wrap(word)
        return [word]
