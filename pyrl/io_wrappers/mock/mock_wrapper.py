from __future__ import annotations

from pyrl.io_wrappers.io_window import IoWindow
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.io_wrappers.mock import IMPLEMENTATION
from pyrl.io_wrappers.mock.mock_window import MockWindow
from pyrl.structures.dimensions import Dimensions

class MockWrapper(IoWrapper):

    implementation = IMPLEMENTATION

    def new_window(self, dimensions: Dimensions) -> IoWindow:
        return MockWindow()

    def flush(self) -> None:
        pass

    def suspend(self) -> None:
        pass

    def resume(self) -> None:
        pass
