from __future__ import division
import os
import pickle
import zlib
import const.game as GAME

def load(save_name):
	save_path = os.path.join(GAME.DATA_FOLDER, save_name)
	with open(save_path, "rb") as f:
		state_string = f.read()
	return pickle.loads(zlib.decompress(state_string))

def save(obj, save_name):
	state_string = pickle.dumps(obj)
	compressed_state = zlib.compress(state_string, 6)
	save_path = os.path.join(GAME.DATA_FOLDER, save_name)
	with open(save_path, "wb") as f:
		f.write(compressed_state)
	save_size = os.path.getsize(save_path)
	uncompressed = len(state_string)

	msg_str = "Savegame file size: {}B uncompressed and {}B compressed with a {:.2%} ratio"
	return msg_str.format(uncompressed, save_size, uncompressed/save_size)
