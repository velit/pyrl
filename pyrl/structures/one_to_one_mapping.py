from __future__ import annotations

from collections import UserDict
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")

class OTOMap(UserDict[K, V]):
    """One to one mapping. A dict-like object which guarantees uniqueness for values in addition to keys."""
    def __setitem__(self, key: K, value: V) -> None:
        if value in self.values():
            raise ValueError(f"{value=} already exists in mapping.")
        super().__setitem__(key, value)

    def getkey(self, value: V) -> K:
        for key, existing_value in self.items():
            if value == existing_value:
                return key
        raise KeyError(f"{value=} not found in mapping.")
