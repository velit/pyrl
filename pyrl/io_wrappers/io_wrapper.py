from __future__ import annotations

from abc import abstractmethod
from typing import Protocol

from pyrl.io_wrappers.io_window import IoWindow
from pyrl.structures.dimensions import Dimensions

class IoWrapper(Protocol):
    implementation: str

    @abstractmethod
    def new_window(self, dimensions: Dimensions) -> IoWindow:
        raise NotImplementedError

    @abstractmethod
    def flush(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def suspend(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def resume(self) -> None:
        raise NotImplementedError
