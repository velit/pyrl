from __future__ import annotations

import logging
import time
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeVar, Callable, TYPE_CHECKING, Any

from pyrl.io_wrappers.io_window import IoWindow
from pyrl.types.key_sequence import KeySequence, AnyKeys
from pyrl.types.keys import Key

if TYPE_CHECKING:
    from pyrl.engine.game import Game

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
class DummyOptions:
    mode:       DummyMode  = DummyMode.Hybrid
    speed_mode: DummySpeed = DummySpeed.Instant
    delay:      float      = 0 # seconds
    log_debug:  bool       = False

@dataclass(eq=False)
class DummyPlugSystem:
    dummy_input: deque[Key] = field(init=False, default_factory=deque)
    options: DummyOptions = field(default_factory=DummyOptions)

    def __enter__(self) -> DummyPlugSystem:
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.reset_options()

    def change_options(self, options: DummyOptions) -> None:
        self.options = options

    def reset_options(self) -> None:
        self.options = DummyOptions()

    def add_input(self, input_iterable: Iterable[Key]) -> None:
        self.dummy_input.extend(input_iterable)

    def add_input_and_run(self, sequence_iterable: AnyKeys, game: Game) -> Game:
        key_iterable = tuple(seq.key if isinstance(seq, KeySequence) else seq for seq in sequence_iterable)
        self.add_input(key_iterable)
        try:
            game.game_loop()
        except StopSimulation:
            return game

    def get_dummy_input(self) -> Key:
        """Return a dummy input key or IndexError if empty"""
        return self.dummy_input.popleft()

_dps = DummyPlugSystem()

def get(options: DummyOptions | None = None) -> DummyPlugSystem:
    if options is not None:
        _dps.change_options(options)
    return _dps

IoWindowSubclass = TypeVar('IoWindowSubclass', bound=IoWindow)
def handle_dummy_input(get_key: Callable[[IoWindowSubclass], Key]) -> Callable[[IoWindowSubclass], Key]:

    def get_key_handle_dummy_input(self: IoWindowSubclass) -> Key:
        """Get a key and handle dummy input if any exist"""
        dps = get()
        if dps.options.mode != DummyMode.Disabled:
            if dps.dummy_input:
                if dps.options.speed_mode == DummySpeed.Delayed:
                    time.sleep(dps.options.delay)
                elif dps.options.speed_mode == DummySpeed.UseInput:
                    get_key(self)
                key = dps.get_dummy_input()
                if dps.options.log_debug:
                    logging.debug(f"Dummy input: {key}")
                return key
            elif dps.options.mode == DummyMode.Full:
                raise StopSimulation()
        key = get_key(self)
        if dps.options.log_debug:
            logging.debug(f"User input: {key}")
        return key

    return get_key_handle_dummy_input
