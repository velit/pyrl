from __future__ import annotations

import bz2
import pickle
from pathlib import Path
from typing import Any

from pyrl.config.config import Config

_SAVE_FILETYPE = ".save"

def load(save_name: str) -> Any:
    save_path = Path(Config.save_folder, save_name + _SAVE_FILETYPE)
    with open(save_path, "rb") as f:
        state_string = f.read()
    return pickle.loads(bz2.decompress(state_string))

def save(obj: Any, save_name: str) -> str:
    Path(Config.save_folder).mkdir(parents=True, exist_ok=True)
    save_path = Path(Config.save_folder, save_name + _SAVE_FILETYPE)
    state, compressed_state = pickle_data(obj)
    with open(save_path, "wb") as f:
        f.write(compressed_state)
    return f"Saved game '{save_path}': {compression_msg(state, compressed_state)}"

def pickle_data(obj: Any) -> tuple[bytes, bytes]:
    state = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    compressed_state = bz2.compress(state, Config.save_compression_level)
    return state, compressed_state

def compression_msg(state: bytes, compressed: bytes) -> str:
    raw_size = sizeof_fmt(len(state))
    compressed_size = sizeof_fmt(len(compressed))
    return f"{compressed_size} / {raw_size:} raw == {len(compressed) / len(state):.1%} compression"

def sizeof_fmt(num: float, suffix: str = "B") -> str:
    for unit in ["", "k", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1000.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
