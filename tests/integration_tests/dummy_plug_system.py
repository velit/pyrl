from __future__ import annotations

import logging
import time
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from types import TracebackType
from typing import TypeVar, Callable, TYPE_CHECKING, Type, Any
from pyrl.io_wrappers.io_window import IoWindow
from pyrl.types.key_sequence import KeySequence, AnyKeys
from pyrl.types.keys import Key

if TYPE_CHECKING:
    from pyrl.game import Game

class StopSimulation(Exception):
    pass

class DummyMode(Enum):
    # Do not use prepared input mechanism at all
    Disabled = 0
    # Use prepared input when given, otherwise fall back to regular input
    Hybrid = 1
    # Use only prepared input and halt the simulation when input ends
    Full = 2

class DummySpeed(Enum):
    # Prepared input is instant
    Instant = 1
    # Use a delay when giving prepared input
    Delayed = 2
    # Use user input as a trigger to feed the prepared input
    UseInput = 3

@dataclass
class DummyPlugSystem:
    dummy_input: deque[Key] = field(init=False, default_factory=deque)
    mode: DummyMode = DummyMode.Hybrid
    speed_mode: DummySpeed = DummySpeed.Instant
    delay: float = 1  # seconds

    def change_modes(self, *, mode: DummyMode | None = None,
                     speed_mode: DummySpeed | None = None,
                     delay: float | None = None) -> None:
        if mode:
            _dps.mode = mode
        if speed_mode:
            _dps.speed_mode = speed_mode
        if delay:
            _dps.delay = delay

    def __enter__(self) -> DummyPlugSystem:
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.reset_modes()

    def reset_modes(self) -> None:
        self.__init__()  # type: ignore

    def get_dummy_input(self) -> Key:
        """Return a dummy input key or IndexError if empty"""
        key = self.dummy_input.popleft()
        logging.debug(f"Dummy input: {key}")
        return key

    def add_input(self, input_iterable: Iterable[Key]) -> None:
        self.dummy_input.extend(input_iterable)

    def add_input_and_run(self, sequence_iterable: AnyKeys, game: Game) -> Game:
        key_iterable = tuple(seq.key if isinstance(seq, KeySequence) else seq for seq in sequence_iterable)
        self.add_input(key_iterable)
        try:
            game.game_loop()
        except StopSimulation:
            return game

_dps = DummyPlugSystem()

def get(*, mode: DummyMode | None = None,
        speed_mode: DummySpeed | None = None,
        delay: float | None = None) -> DummyPlugSystem:
    _dps.change_modes(mode=mode, speed_mode=speed_mode, delay=delay)
    return _dps

IoWindowSubclass = TypeVar('IoWindowSubclass', bound=IoWindow)
def handle_dummy_input(get_key: Callable[[IoWindowSubclass], Key]) -> Callable[[IoWindowSubclass], Key]:

    def get_key_handle_dummy_input(self: IoWindowSubclass) -> Key:
        """Get a key and handle dummy input if any exist"""
        if get().mode != DummyMode.Disabled:
            if get().dummy_input:
                if get().speed_mode == DummySpeed.Delayed:
                    time.sleep(get().delay)
                elif get().speed_mode == DummySpeed.UseInput:
                    get_key(self)
                return get().get_dummy_input()
            elif get().mode == DummyMode.Full:
                raise StopSimulation()
        return get_key(self)

    return get_key_handle_dummy_input
