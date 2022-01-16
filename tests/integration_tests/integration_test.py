from __future__ import annotations

from collections.abc import Iterable

import pytest

from pyrl import main
from pyrl.config.binds import Binds
from pyrl.game import Game
from pyrl.io_wrappers.io_wrapper import IoWrapper
# from pyrl.io_wrappers.tcod.tcod_wrapper import TcodWrapper as TestWrapper
from pyrl.io_wrappers.mock.mock_wrapper import MockWrapper as TestWrapper
from pyrl.types.key_sequence import AnyKeys
from tests.integration_tests import dummy_plug_system
from tests.integration_tests.dummy_plug_system import DummySpeed, DummyMode, DummyPlugSystem, DummyOptions

# CONTINUE_AFTER_INTEGRATION_TEST = True
CONTINUE_AFTER_INTEGRATION_TEST = False

@pytest.fixture
def dummy() -> Iterable[DummyPlugSystem]:
    # with dummy_plug_system.get(DummyOptions(mode=DummyMode.Full, speed_mode=DummySpeed.Delayed, delay=0.1)) as dummy_plug:
    with dummy_plug_system.get(DummyOptions(mode=DummyMode.Full, speed_mode=DummySpeed.Instant)) as dummy_plug:
        yield dummy_plug

@pytest.fixture
def io_wrapper() -> Iterable[IoWrapper]:
    with TestWrapper() as io_wrapper:
        yield io_wrapper

@pytest.fixture
def game(io_wrapper: IoWrapper) -> Game:
    return main.create_game(main.get_commandline_options(args=("-g", "test")), io_wrapper)

def load_game(io_wrapper: IoWrapper) -> Game:
    return main.create_game(main.get_commandline_options(args=("-l", "test")), io_wrapper)

def test_save_and_load_game(game: Game, io_wrapper: IoWrapper, dummy: DummyPlugSystem) -> None:

    input_seq = [Binds.Descend] * 4 + [Binds.Save]
    game = dummy.add_input_and_run(input_seq, game)
    assert game.turn_counter == 4
    assert game.player.level.level_key.idx == 3

    game = load_game(io_wrapper)
    input_seq = [Binds.Descend] * 4
    game = dummy.add_input_and_run(input_seq, game)
    assert game.turn_counter == 8
    assert game.player.level.level_key.idx == 5

def test_subsystems(game: Game, dummy: DummyPlugSystem) -> None:

    if game.io.wrapper.implementation != "mock" and CONTINUE_AFTER_INTEGRATION_TEST:
        old_mode = dummy.options.mode
        dummy.options.mode = DummyMode.Disabled
        game.io.get_key()
        dummy.options.mode = old_mode

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
    message_system: AnyKeys = [Binds.Debug_Commands, 'm', Binds.Skip_To_Last_Message]
    whole_map: AnyKeys = [Binds.Debug_Commands, 'v']
    path_to_staircase: AnyKeys = [Binds.Debug_Commands, 'o', Binds.Skip_To_Last_Message]

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
    )

    walk_mode = [Binds.Walk_Mode, Binds.East]

    descend = [Binds.Descend, Binds.Descend]

    coord = game.player.coord

    game = dummy.add_input_and_run(help_system, game)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = dummy.add_input_and_run(help_system, game)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = dummy.add_input_and_run(movement_and_look_system, game)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = dummy.add_input_and_run(message_system, game)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = dummy.add_input_and_run(whole_map, game)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = dummy.add_input_and_run(path_to_staircase, game)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    previous_bag_count = len(game.player.inventory._bag)
    game = dummy.add_input_and_run(inventory, game)
    assert game.turn_counter == 3
    assert coord == game.player.coord
    assert len(game.player.inventory._bag) == previous_bag_count + 2

    game = dummy.add_input_and_run(walk_mode, game)
    assert game.turn_counter == 7

    game = dummy.add_input_and_run(descend, game)
    assert game.turn_counter == 9
    assert game.player.level.level_key.idx == 2

    # equip armor
    game = dummy.add_input_and_run(['e', 'b', 'a', 'z'], game)
    # run to end
    # game = dummy.add_input_and_run(['d', 'x'], game)

    if CONTINUE_AFTER_INTEGRATION_TEST:
        dummy.reset_options()
        with pytest.raises(SystemExit) as _:
            game.game_loop()
    elif dummy.options.speed_mode != DummySpeed.Instant:
        dummy.options.mode = DummyMode.Hybrid
        game.io.get_key()
