from __future__ import annotations

from pathlib import Path


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
