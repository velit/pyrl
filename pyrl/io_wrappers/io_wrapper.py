from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, Any, ClassVar

from pyrl.io_wrappers.io_window import IoWindow
from pyrl.structures.dimensions import Dimensions

class IoWrapper(Protocol):
    implementation: ClassVar[str]

    def __enter__(self) -> IoWrapper:
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def new_window(self, dimensions: Dimensions) -> IoWindow:
        raise NotImplementedError

    def flush(self) -> None:
        pass

    def suspend(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def toggle_fullscreen(self) -> None:
        pass

    def next_tileset(self) -> str:
        return f"Not supported in {self.implementation}"

    def previous_tileset(self) -> str:
        return f"Not supported in {self.implementation}"

    def next_bdf(self) -> str:
        return f"Not supported in {self.implementation}"

    def previous_bdf(self) -> str:
        return f"Not supported in {self.implementation}"
