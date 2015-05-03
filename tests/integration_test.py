from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
from io_wrappers.mock import MockInputEnd
from enums.keys import Key


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

    input_seq = "X" * 4 + "S"
    game = prepare_input_and_exe(mockwrapper, game, input_seq)
    assert game.turn_counter == 4
    assert game.player.level.world_loc[1] == 3

    game = load_game(mockwrapper)
    input_seq = "X" * 4
    game = prepare_input_and_exe(mockwrapper, game, input_seq)
    assert game.turn_counter == 8
    assert game.player.level.world_loc[1] == 5


def test_subsystems(mockwrapper, game):

    look_system = tuple("q4862q")
    help_system = (Key.F1, "z")
    message_system = ('d', 'm', Key.ENTER)
    whole_map = tuple("dv")
    path_to_staircase = ('d', 'o', Key.ENTER)
    inventory = tuple("ivzbrlaz")
    walk_mode = tuple("w6")
    input_seq = help_system + look_system + message_system + whole_map + path_to_staircase + inventory + walk_mode
    game = prepare_input_and_exe(mockwrapper, game, input_seq)
    assert game.turn_counter == 4
