from __future__ import annotations

from typing import Iterable

from pyrl.types.keys import Key

class KeySequence(tuple[Key, ...]):

    def __new__(cls, key_or_iterable: Key | Iterable[Key] = (), /) -> KeySequence:
        if isinstance(key_or_iterable, Key):
            return super().__new__(cls, (key_or_iterable,))  # type: ignore
        else:
            return super().__new__(cls, key_or_iterable)  # type: ignore

    @property
    def key(self) -> Key:
        if len(self):
            return self[0]
        else:
            return "Unbound"

    def __str__(self) -> str:
        return "/".join(f"{key}" for key in self)

AnyKey = Key | KeySequence
AnyKeys = Iterable[Key | KeySequence]
