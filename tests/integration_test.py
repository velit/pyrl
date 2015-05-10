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


def prepare_input_and_exe(mockwrapper, game, input_seq):
    mockwrapper._prepare_input(input_seq)
    try:
        game.main_loop()
        assert False
    except MockInputEnd:
        return game


def test_save_and_load_game(mockwrapper, game):

    input_seq = [Bind.Descend.key] * 4 + [Bind.Save.key]
    game = prepare_input_and_exe(mockwrapper, game, input_seq)
    assert game.turn_counter == 4
    assert game.player.level.world_loc[1] == 3

    game = load_game(mockwrapper)
    input_seq = [Bind.Descend.key] * 4
    game = prepare_input_and_exe(mockwrapper, game, input_seq)
    assert game.turn_counter == 8
    assert game.player.level.world_loc[1] == 5


def test_subsystems(mockwrapper, game):

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
    message_system = ('d', 'm', Bind.Last_Message)
    whole_map = ('d', 'v')
    path_to_staircase = ('d', 'o', Bind.Last_Message)

    inventory = (
        Bind.Inventory,
        Bind.View_Inventory,
        Bind.Cancel,
        Bind.Equipment_Slot_Body,
        Bind.Equipment_Slot_Right_Hand,
        Bind.Equipment_Slot_Left_Hand,
        Bind.Item_Select_Keys[0],
        Bind.Cancel,
    )

    walk_mode = (Bind.Walk_Mode, Bind.East, Bind.Instant_West)

    input_seq = help_system + movement_and_look_system + message_system + whole_map + path_to_staircase + inventory + walk_mode
    input_seq = (action if isinstance(action, str) else action.key for action in input_seq)
    game = prepare_input_and_exe(mockwrapper, game, input_seq)
    assert game.turn_counter == 4
