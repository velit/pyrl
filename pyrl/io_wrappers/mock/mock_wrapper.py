from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from pyrl.io_wrappers.mock import IMPLEMENTATION
from pyrl.io_wrappers.mock.mock_window import MockWindow
from pyrl.structures.dimensions import Dimensions
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.io_wrappers.io_window import IoWindow

class MockInputEnd(Exception):
    pass

class MockWrapper(IoWrapper):

    implementation = IMPLEMENTATION

    def __init__(self) -> None:
        self._prepared_input: deque[str] = deque()

    def new_window(self, dimensions: Dimensions) -> IoWindow:
        return MockWindow(self)

    def flush(self) -> None:
        pass

    def suspend(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def prepare_input(self, input_seq: Iterable[str]) -> None:
        self._prepared_input.extend(input_seq)

