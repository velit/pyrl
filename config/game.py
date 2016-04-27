from __future__ import absolute_import, division, print_function, unicode_literals


class GameConf(object):

    """Configure variables above the data section to suit your needs."""

    # minimum (30, 96)
    game_dimensions        = (30, 96)

    # valid between 1 and 9, higher slower but less space
    save_compression_level = 6

    message_bar_height     = 2
    status_bar_height      = 2
    animation_period       = 0.005
    default_game_name      = "pyrl"
    clearly_show_vision    = False

    ##################################
    ### Data section, don't modify ###
    ##################################

    DATA_FOLDER = "save_data"
    LEVEL_DIMENSIONS = (game_dimensions[0] - message_bar_height - status_bar_height, game_dimensions[1])
    ANIMATION_INPUT_PERIOD = min(animation_period / 10, 0.001)
