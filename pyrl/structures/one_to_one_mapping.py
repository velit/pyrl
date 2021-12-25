from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')
class OneToOneMapping(dict[K, V]):

    """A dict-like object which guarantees uniqueness for values in addition to keys."""

    def __setitem__(self, key: K, value: V) -> None:
        if value in self.values():
            raise ValueError(f"{value=} already exists in mapping.")
        super().__setitem__(key, value)

    def getkey(self, value: V) -> K:
        for key, existing_value in self.items():
            if value == existing_value:
                return key
        raise KeyError(f"{value=} not found in mapping.")

    def update(self, arg: dict[K, V] | Iterable[tuple[K, V]] | None = None, **kwords: dict[str, V]) -> None:
        if arg is not None:
            if isinstance(arg, dict):
                for key in arg:
                    self[key] = arg[key]
            else:
                for key, value in arg:
                    self[key] = value
        for key in kwords:
            self[key] = kwords[key]
