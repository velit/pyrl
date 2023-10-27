from __future__ import annotations

import tomllib
from pathlib import Path

from importlib.resources import files


class Config:
    """Configure variables above the data section to suit your needs."""

    # valid between 1 and 9, higher slower but less space
    save_compression_level = 9

    message_bar_height = 2
    status_bar_height = 2
    animation_period = 0.005
    default_game_name = "pyrl"
    clearly_show_vision = False
    save_folder = Path("save_data")
    secret_path = save_folder / ".do_not_share_this_file"
    save_game_warning = True

with files("pyrl").joinpath("config.toml").open("rb") as config_file:
    config = tomllib.load(config_file)
    if "save_game_warning" in config:
        Config.save_game_warning = config["save_game_warning"]