from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
from io_wrappers.mock import MockInputEndError


TEST_GAME_NAME = "test"


@pytest.fixture
def mockwrapper():
    from io_wrappers.mock import MockWrapper
    return MockWrapper


@pytest.fixture
def game(mockwrapper):

    import main
    return main.prepare_game(mockwrapper, cmdline_args=("-g", TEST_GAME_NAME))


def load_game(mockwrapper):

    import main
    return main.prepare_game(mockwrapper, cmdline_args=("-l", TEST_GAME_NAME))


def prepare_input_and_exe(mockwrapper, game, input_seq):
    mockwrapper._prepare_input(input_seq)
    try:
        game.main_loop()
        assert False
    except MockInputEndError:
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
