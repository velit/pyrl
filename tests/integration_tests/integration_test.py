from __future__ import annotations

import platform
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Type

import pytest

from pyrl import main
from pyrl.config.binds import Binds
from pyrl.engine.game import Game
from pyrl.engine.enums.keys import KeyOrSequence
from pyrl.ui.io_lib.protocol.io_wrapper import IoWrapper
from tests.integration_tests import dummy_plug_system
from tests.integration_tests.dummy_plug_system import DummySpeed, DummyMode, DummyPlugSystem, DummyOptions

@dataclass
class IntegrConfig:
    io_wrapper_type: Type[IoWrapper]
    continue_after_test: bool
    dummy_options: DummyOptions

@pytest.fixture
def live_config(delay: float) -> IntegrConfig:
    from pyrl.ui.io_lib.tcod.tcod_wrapper import TcodWrapper
    dummy_options = DummyOptions(mode=DummyMode.Override,
                                 speed_mode=DummySpeed.Delayed,
                                 delay=delay,
                                 log_debug=False)
    return IntegrConfig(io_wrapper_type=TcodWrapper,
                        continue_after_test=True,
                        dummy_options=dummy_options)

@pytest.fixture
def background_config() -> IntegrConfig:
    from pyrl.ui.io_lib.mock.mock_wrapper import MockWrapper
    dummy_options = DummyOptions(mode=DummyMode.Override,
                                 speed_mode=DummySpeed.Instant,
                                 delay=0,
                                 log_debug=False)
    return IntegrConfig(io_wrapper_type=MockWrapper,
                        continue_after_test=False,
                        dummy_options=dummy_options)

@pytest.fixture
def integr_config(live: bool, live_config: IntegrConfig, background_config: IntegrConfig) -> IntegrConfig:
    if live:
        return live_config
    return background_config

@pytest.fixture
def dummy_system(integr_config: IntegrConfig) -> Iterable[DummyPlugSystem]:
    with dummy_plug_system.get(integr_config.dummy_options) as dummy_plug:
        yield dummy_plug

@pytest.fixture
def io_wrapper(integr_config: IntegrConfig) -> Iterable[IoWrapper]:
    with integr_config.io_wrapper_type() as io_wrapper:
        yield io_wrapper

@pytest.fixture
def game(io_wrapper: IoWrapper, dummy_system: DummyPlugSystem, integr_config: IntegrConfig) -> Iterable[Game]:
    game = main.create_game(main.get_commandline_options(args=("-g", "test")), io_wrapper)
    if platform.system() == "Darwin" and game.io.wrapper.implementation != "mock" and integr_config.continue_after_test:
        old_mode = dummy_system.options.mode
        dummy_system.options.mode = DummyMode.Disabled
        # Macos for some reason needs the window to be in a waiting state for it to render before the end of the tests
        game.io.get_key("Press any key to start the test.")
        dummy_system.options.mode = old_mode

    yield game

    if integr_config.continue_after_test:
        dummy_system.reset_options()
        with pytest.raises(SystemExit) as _:
            game.io.msg("Test successful.")
            game.game_loop()
    elif dummy_system.options.speed_mode != DummySpeed.Instant:
        dummy_system.options.mode = DummyMode.Hybrid
        game.io.get_key()

def load_game(io_wrapper: IoWrapper) -> Game:
    return main.create_game(main.get_commandline_options(args=("-l", "test")), io_wrapper)

def test_save_and_load_game(game: Game, io_wrapper: IoWrapper, dummy_system: DummyPlugSystem) -> None:

    input_seq = [Binds.Descend] * 4 + [Binds.Save]
    game = dummy_system.add_input_and_run(input_seq, game)
    assert game.player.turns == 5
    assert game.player.level.level_key.idx == 3

    game = load_game(io_wrapper)
    input_seq = [Binds.Descend] * 4
    game = dummy_system.add_input_and_run(input_seq, game)
    assert game.player.turns == 9
    assert game.player.level.level_key.idx == 5

def test_subsystems(integr_config: IntegrConfig, game: Game, dummy_system: DummyPlugSystem) -> None:

    help_system = (Binds.Help, Binds.Cancel)

    movement_and_look_system = (
        Binds.Look_Mode,
        Binds.North,
        Binds.South,
        Binds.NorthEast,
        Binds.SouthWest,
        Binds.West,
        Binds.East,
        Binds.SouthEast,
        Binds.NorthWest,
        Binds.Stay,
        Binds.Look_Mode,
    )

    # debug_actions enabled ones
    message_system: Iterable[KeyOrSequence] = [Binds.Debug_Commands, 'm', Binds.Skip_To_Last_Message]
    whole_map: Iterable[KeyOrSequence] = [Binds.Debug_Commands, 'v']
    path_to_staircase: Iterable[KeyOrSequence] = [Binds.Debug_Commands, 'o', Binds.Skip_To_Last_Message]

    inventory = (
        Binds.Equipment,
        Binds.Equipment_View_Backpack,
        Binds.Cancel,
        Binds.Equipment_Select_Body,
        Binds.Equipment_Select_Right,
        Binds.Equipment_Select_Left,
        Binds.Equipment_Select_Left,
        Binds.Backpack_Select_Keys[0],
        Binds.Cancel,
        Binds.Drop_Items,
        Binds.Backpack_Select_Keys[0],
        Binds.Cancel,
        Binds.Drop_Items,
        Binds.Backpack_Select_Keys[0],
        Binds.Backpack_Select_Keys[1],
        Binds.Backpack_Select_Keys[2],
        Binds.Cancel,
        Binds.Pick_Up_Items,
        Binds.Backpack_Select_Keys[0],
        Binds.Backpack_Select_Keys[1],
        Binds.Backpack_Select_Keys[2],
        Binds.Backpack_Select_Keys[3],
        Binds.Cancel,
        Binds.Equipment,
        Binds.Equipment_Select_Body,
        Binds.Backpack_Select_Keys[0],
        Binds.Cancel,
    )

    walk_mode = [Binds.Walk_Mode, Binds.East]

    descend = [Binds.Descend, Binds.Descend]

    coord = game.player.coord

    game = dummy_system.add_input_and_run(help_system, game)
    assert game.player.turns == 1
    assert coord == game.player.coord

    game = dummy_system.add_input_and_run(movement_and_look_system, game)
    assert game.player.turns == 1
    assert coord == game.player.coord

    game = dummy_system.add_input_and_run(message_system, game)
    assert game.player.turns == 1
    assert coord == game.player.coord

    game = dummy_system.add_input_and_run(whole_map, game)
    assert game.player.turns == 1
    assert coord == game.player.coord

    game = dummy_system.add_input_and_run(path_to_staircase, game)
    assert game.player.turns == 1
    assert coord == game.player.coord

    previous_bag_count = len(game.player.inventory._bag)
    game = dummy_system.add_input_and_run(inventory, game)
    assert game.player.turns == 4
    assert coord == game.player.coord
    assert len(game.player.inventory._bag) == previous_bag_count + 1

    game = dummy_system.add_input_and_run(walk_mode, game)
    assert game.player.turns == 8

    game = dummy_system.add_input_and_run(descend, game)
    assert game.player.turns == 10
    assert game.player.level.level_key.idx == 2

    # run to end
    # game = dummy.add_input_and_run(['d', 'x'], game)
