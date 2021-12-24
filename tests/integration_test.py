from __future__ import annotations

import pytest

from pyrl import main
from pyrl.binds import Binds
from pyrl.io_wrappers.mock import MockInputEnd

TEST_GameConf_NAME = "test"

@pytest.fixture
def mock_wrapper():
    from pyrl.io_wrappers.mock import MockWrapper
    return MockWrapper()

@pytest.fixture
def game(mock_wrapper):
    return main.create_game(main.get_commandline_options(args=("-g", TEST_GameConf_NAME)), mock_wrapper)

def load_game(mock_wrapper):
    return main.create_game(main.get_commandline_options(args=("-l", TEST_GameConf_NAME)), mock_wrapper)

def prepare_input_and_run(game, input_seq):
    input_seq = tuple(action if isinstance(action, str) else action.key for action in input_seq)
    game.io.cursor_lib.prepare_input(input_seq)
    try:
        game.game_loop()
        assert False
    except MockInputEnd:
        return game

@pytest.mark.skip(reason="Disabled until save system is fixed")
def test_save_and_load_game(game, mock_wrapper):

    input_seq = [Binds.Descend] * 4 + [Binds.Save]
    game = prepare_input_and_run(game, input_seq)
    assert game.turn_counter == 4
    assert game.player.level.level_key.index == 3

    game = load_game(mock_wrapper)
    input_seq = [Binds.Descend] * 4
    game = prepare_input_and_run(game, input_seq)
    assert game.turn_counter == 8
    assert game.player.level.level_key.index == 5

def test_subsystems(game):

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
    message_system = (Binds.Debug_Commands, 'm', Binds.Skip_To_Last_Message)
    whole_map = (Binds.Debug_Commands, 'v')
    path_to_staircase = (Binds.Debug_Commands, 'o', Binds.Skip_To_Last_Message)

    inventory = (
        Binds.Equipment,
        Binds.Equipment_View_Backpack,
        Binds.Cancel,
        Binds.Equipment_Select_Keys[1],
        Binds.Equipment_Select_Keys[2],
        Binds.Equipment_Select_Keys[3],
        Binds.Equipment_Select_Keys[3],
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

    walk_mode = (Binds.Walk_Mode, Binds.East)

    coord = game.player.coord

    game = prepare_input_and_run(game, help_system)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = prepare_input_and_run(game, help_system)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = prepare_input_and_run(game, movement_and_look_system)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = prepare_input_and_run(game, message_system)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = prepare_input_and_run(game, whole_map)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    game = prepare_input_and_run(game, path_to_staircase)
    assert game.turn_counter == 0
    assert coord == game.player.coord

    previous_bag_count = len(game.player.inventory._bag)
    game = prepare_input_and_run(game, inventory)
    assert game.turn_counter == 3
    assert coord == game.player.coord
    assert len(game.player.inventory._bag) == previous_bag_count + 2

    game = prepare_input_and_run(game, walk_mode)
    assert game.turn_counter == 7
