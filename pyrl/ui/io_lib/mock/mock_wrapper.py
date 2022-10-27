from __future__ import annotations

from pyrl.engine.structures.dimensions import Dimensions
from pyrl.ui.io_lib.mock import IMPLEMENTATION
from pyrl.ui.io_lib.mock.mock_window import MockWindow
from pyrl.ui.io_lib.protocol.io_window import IoWindow
from pyrl.ui.io_lib.protocol.io_wrapper import IoWrapper

class MockWrapper(IoWrapper):
    __test__ = False

    implementation = IMPLEMENTATION

    def new_window(self, dimensions: Dimensions) -> IoWindow:
        return MockWindow()
