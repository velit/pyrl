from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, Any, ClassVar

from pyrl.engine.structures.dimensions import Dimensions
from pyrl.ui.io_lib.protocol.io_window import IoWindow

class IoWrapper(Protocol):
    implementation: ClassVar[str]

    def __enter__(self) -> IoWrapper:
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        return

    @abstractmethod
    def new_window(self, dimensions: Dimensions) -> IoWindow:
        raise NotImplementedError

    def flush(self) -> None:
        return

    def suspend(self) -> None:
        return

    def resume(self) -> None:
        return

    def toggle_fullscreen(self) -> None:
        return

    def next_tileset(self) -> str:
        return f"Not supported in {self.implementation}"

    def previous_tileset(self) -> str:
        return f"Not supported in {self.implementation}"

    def next_bdf(self) -> str:
        return f"Not supported in {self.implementation}"

    def previous_bdf(self) -> str:
        return f"Not supported in {self.implementation}"
