from __future__ import absolute_import, division, print_function, unicode_literals

import os
import pickle
import bz2

from config.game import GameConf


_SAVE_FILETYPE = ".svg"


def load(save_name):
    save_path = os.path.join(GameConf.DATA_FOLDER, save_name + _SAVE_FILETYPE)
    with open(save_path, "rb") as f:
        state_string = f.read()
    return pickle.loads(bz2.decompress(state_string))


def save(obj, save_name):
    if not os.path.exists(GameConf.DATA_FOLDER):
        os.mkdir(GameConf.DATA_FOLDER)

    save_path = os.path.join(GameConf.DATA_FOLDER, save_name + _SAVE_FILETYPE)
    state_string = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    compressed_state = bz2.compress(state_string, GameConf.save_compression_level)
    with open(save_path, "wb") as f:
        f.write(compressed_state)

    save_size = os.path.getsize(save_path)
    uncompressed = len(state_string)

    return uncompressed, save_size
