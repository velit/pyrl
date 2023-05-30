from __future__ import annotations

import logging
import time
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from functools import partial
from typing import TypeVar, Callable, TYPE_CHECKING, Any

from pyrl.engine.types.keys import AnyKey, KeySequence, KeyOrSequence
from pyrl.ui.io_lib.protocol.io_window import IoWindow

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
    Override = 2

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
    dummy_input: deque[AnyKey] = field(init=False, default_factory=deque)
    options: DummyOptions = field(default_factory=DummyOptions)

    def __enter__(self) -> DummyPlugSystem:
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.reset()

    def change_options(self, options: DummyOptions) -> None:
        self.options = options

    def reset(self) -> None:
        self.dummy_input = deque()
        self.reset_options()

    def reset_options(self) -> None:
        self.options = DummyOptions()

    def add_input(self, input_iterable: Iterable[AnyKey]) -> None:
        self.dummy_input.extend(input_iterable)

    def add_input_and_run(self, sequence_iterable: Iterable[KeyOrSequence], game: Game) -> Game:
        key_iterable = tuple(seq.key if isinstance(seq, KeySequence) else seq for seq in sequence_iterable)
        self.add_input(key_iterable)
        try:
            game.game_loop()
        except StopSimulation:
            return game

    def get_dummy_input(self) -> AnyKey:
        """Return a dummy input key or IndexError if empty"""
        return self.dummy_input.popleft()

_rei = DummyPlugSystem()

def get(options: DummyOptions | None = None) -> DummyPlugSystem:
    if options is not None:
        _rei.change_options(options)
    return _rei

IoWindowSubclass = TypeVar('IoWindowSubclass', bound=IoWindow)
GetKeyMethod = Callable[[IoWindowSubclass], AnyKey]
def handle_dummy_input(get_key: GetKeyMethod[IoWindowSubclass]) -> GetKeyMethod[IoWindowSubclass]:

    def get_key_handle_dummy_input(self: IoWindowSubclass) -> AnyKey:
        """Get a key and handle dummy input if any exist"""
        dps = get()
        bound_get_key = get_key.__get__(self, self.__class__)

        def _get_key(key_getter: Callable[[], AnyKey], input_mode: str) -> AnyKey:
            key = key_getter()
            if dps.options.log_debug:
                logging.debug(f"{input_mode} input: {key}")
            return key

        if dps.options.mode != DummyMode.Disabled and dps.dummy_input:
            if dps.options.speed_mode == DummySpeed.Delayed:
                time.sleep(dps.options.delay)
            elif dps.options.speed_mode == DummySpeed.UseInput:
                bound_get_key()
            return _get_key(dps.get_dummy_input, "Dummy")

        elif dps.options.mode == DummyMode.Override:
            raise StopSimulation()

        return _get_key(bound_get_key, "User")

    return get_key_handle_dummy_input
