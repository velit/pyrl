from __future__ import absolute_import, division, print_function, unicode_literals


import pytest


@pytest.fixture
def game_and_mockwrapper():

    import main
    from io_wrappers.mock import MockWrapper

    main.init_window_system(MockWrapper)
    game = main.prepare_game(cmdline_arg_string="")

    return game, main.io.cursor_lib


def prepare_input_and_exe(game_and_mockwrapper, input_seq):
    from io_wrappers.mock import MockInputEndError
    game, mockwrapper = game_and_mockwrapper
    mockwrapper._prepare_input(input_seq)
    try:
        game.main_loop()
        assert False
    except MockInputEndError:
        return game


def test_iterate_levels(game_and_mockwrapper):

    input_seq = "X" * 18
    game = prepare_input_and_exe(game_and_mockwrapper, input_seq)
    assert game.turn_counter == 18
    assert game.player.level.world_loc[1] == 10


def test_save_game(game_and_mockwrapper):

    input_seq = "X" * 18 + "S"
    game = prepare_input_and_exe(game_and_mockwrapper, input_seq)
    assert game.turn_counter == 18
    assert game.player.level.world_loc[1] == 10
