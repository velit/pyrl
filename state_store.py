from __future__ import absolute_import, division, print_function, unicode_literals

import os
import pickle
import zlib

import const.game as GAME


_SAVE_FILETYPE = ".svg"


def load(save_name):
    save_path = os.path.join(GAME.DATA_FOLDER, save_name + _SAVE_FILETYPE)
    with open(save_path, "rb") as f:
        state_string = f.read()
    return pickle.loads(zlib.decompress(state_string))


def save(obj, save_name):
    if not os.path.exists(GAME.DATA_FOLDER):
        os.mkdir(GAME.DATA_FOLDER)

    save_path = os.path.join(GAME.DATA_FOLDER, save_name + _SAVE_FILETYPE)
    state_string = pickle.dumps(obj)
    compressed_state = zlib.compress(state_string, GAME.SAVE_FILE_COMPRESSION_LEVEL)
    with open(save_path, "wb") as f:
        f.write(compressed_state)

    save_size = os.path.getsize(save_path)
    uncompressed = len(state_string)

    return uncompressed, save_size
    return msg_str.format(uncompressed, save_size, uncompressed / save_size)
