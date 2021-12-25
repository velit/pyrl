from __future__ import annotations

import bz2
import os
import pickle

from pyrl.config.config import Config
from pyrl.game import Game

_SAVE_FILETYPE = ".svg"

def load(save_name: str) -> Game:
    save_path = os.path.join(Config.save_folder, save_name + _SAVE_FILETYPE)
    with open(save_path, "rb") as f:
        state_string = f.read()
    return pickle.loads(bz2.decompress(state_string))

def save(game: Game, save_name: str) -> tuple[int, int]:
    if not os.path.exists(Config.save_folder):
        os.mkdir(Config.save_folder)

    save_path = os.path.join(Config.save_folder, save_name + _SAVE_FILETYPE)
    state_string = pickle.dumps(game, protocol=pickle.HIGHEST_PROTOCOL)
    compressed_state = bz2.compress(state_string, Config.save_compression_level)
    with open(save_path, "wb") as f:
        f.write(compressed_state)

    save_size = os.path.getsize(save_path)
    uncompressed = len(state_string)

    return uncompressed, save_size
