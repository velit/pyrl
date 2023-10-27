from __future__ import annotations

import bz2
import hashlib
import hmac
import pickle
import secrets
import uuid
from pathlib import Path
from typing import Any

from pyrl.config.config import Config

_SAVE_FILETYPE = ".save"

DIGEST_SIZE = 64

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
    digest = create_digest(compressed_state)
    assert len(digest) == DIGEST_SIZE, \
        f"The dev's assumption that blake2 digest would always be {DIGEST_SIZE} bytes long is incorrect"
    return state, digest + compressed_state

def load(save_name: str, unsafe: bool = False) -> Any:
    save_path = Path(Config.save_folder, save_name + _SAVE_FILETYPE)
    with open(save_path, "rb") as f:
        return unpickle_data(f.read(), unsafe)

def unpickle_data(data: bytes, unsafe: bool = False) -> Any:
    digest, compressed_state = data[:DIGEST_SIZE], data[DIGEST_SIZE:]
    expected_digest = create_digest(compressed_state)
    if not unsafe and not secrets.compare_digest(digest, expected_digest):
        raise ValueError("Wrong save file signature. Either hardware has changed or save files were moved.")
    return pickle.loads(bz2.decompress(compressed_state))

def create_digest(data: bytes) -> bytes:
    return hmac.digest(secret(), data, hashlib.blake2b)

def secret() -> bytes:
    return machine_secret() + unique_secret()

def machine_secret() -> bytes:
    return str(uuid.getnode()).encode()

def unique_secret() -> bytes:
    if not Config.secret_path.exists():
        with Config.secret_path.open("wb") as f:
            f.write(secrets.token_bytes(64))
    with Config.secret_path.open("rb") as f:
        return f.read()

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