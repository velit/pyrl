from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Any

@dataclass(eq=False)
class Event:

    observers: list[Callable[..., None]] = field(default_factory=list)

    def subscribe(self, function: Callable[..., None]) -> None:
        self.observers.append(function)

    def unsubscribe(self, function: Callable[..., None]) -> None:
        self.observers.remove(function)

    def trigger(self, *args: Any, **kwargs: Any) -> None:
        for observer in self.observers:
            observer(*args, **kwargs)
