from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
from io_wrappers.mock import MockInputEnd
from config.bindings import Bind


TEST_GameConf_NAME = "test"


@pytest.fixture
def mockwrapper():
    from io_wrappers.mock import MockWrapper
    return MockWrapper


@pytest.fixture
def game(mockwrapper):

    import main
    return main.prepare_game(mockwrapper, cmdline_args=("-g", TEST_GameConf_NAME))


def load_game(mockwrapper):

    import main
    return main.prepare_game(mockwrapper, cmdline_args=("-l", TEST_GameConf_NAME))


def prepare_input_and_run(game, input_seq):
    input_seq = tuple(action if isinstance(action, str) else action.key for action in input_seq)
    game.io.cursor_lib._prepare_input(input_seq)
    try:
        game.main_loop()
        assert False
    except MockInputEnd:
        return game


def test_save_and_load_game(game, mockwrapper):

    input_seq = [Bind.Descend] * 4 + [Bind.Save]
    game = prepare_input_and_run(game, input_seq)
    assert game.turn_counter == 4
    assert game.player.level.key[1] == 3

    game = load_game(mockwrapper)
    input_seq = [Bind.Descend] * 4
    game = prepare_input_and_run(game, input_seq)
    assert game.turn_counter == 8
    assert game.player.level.key[1] == 5


def test_subsystems(game):

    help_system = (Bind.Help, Bind.Cancel)

    movement_and_look_system = (
        Bind.Look_Mode,
        Bind.North,
        Bind.South,
        Bind.NorthEast,
        Bind.SouthWest,
        Bind.West,
        Bind.East,
        Bind.SouthEast,
        Bind.NorthWest,
        Bind.Stay,
        Bind.Look_Mode,
    )

    # debug_actions enabled ones
    message_system = (Bind.Debug_Commands, 'm', Bind.Last_Message)
    whole_map = (Bind.Debug_Commands, 'v')
    path_to_staircase = (Bind.Debug_Commands, 'o', Bind.Last_Message)

    inventory = (
        Bind.Equipment,
        Bind.Equipment_View_Backpack,
        Bind.Cancel,
        Bind.Equipment_Select_Keys[1],
        Bind.Equipment_Select_Keys[2],
        Bind.Equipment_Select_Keys[3],
        Bind.Backpack_Select_Keys[0],
        Bind.Cancel,
        Bind.Drop_Items,
        Bind.Backpack_Select_Keys[0],
        Bind.Cancel,
        Bind.Drop_Items,
        Bind.Backpack_Select_Keys[0],
        Bind.Backpack_Select_Keys[1],
        Bind.Backpack_Select_Keys[2],
        Bind.Cancel,
        Bind.Pick_Up_Items,
        Bind.Backpack_Select_Keys[0],
        Bind.Backpack_Select_Keys[1],
        Bind.Backpack_Select_Keys[2],
        Bind.Backpack_Select_Keys[3],
        Bind.Cancel,
    )

    walk_mode = (Bind.Walk_Mode, Bind.East)

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

    previous_bag_count = len(game.player.equipment._bag)
    game = prepare_input_and_run(game, inventory)
    assert game.turn_counter == 3
    assert coord == game.player.coord
    assert previous_bag_count + 1 == len(game.player.equipment._bag)

    game = prepare_input_and_run(game, walk_mode)
    assert game.turn_counter == 7
