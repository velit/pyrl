import const.game as GAME
import const.tiles as TILE


def gettile(handle, tile_dict=None):
	if tile_dict is not None and handle in tile_dict:
		return tile_dict[handle]
	elif handle in TILE.tiles:
		return TILE.tiles[handle]
	else:
		raise KeyError("Handle '{}' not in global tiles nor in '{}'".format(handle, tile_dict))


class LevelFile(object):

	def __init__(self, danger_level=0, static=False, tilefile=None,
				rows=GAME.LEVEL_HEIGHT, cols=GAME.LEVEL_WIDTH):
		self.danger_level = danger_level
		self.tilefile = tilefile
		self.static = static
		self.rows = rows
		self.cols = cols
		self.passage_locations = {}
		self.monster_files = []
		self.tile_dict = {}

	def get_tile_id(self, y, x):
		return self.tilefile[self.getloc(y, x)]

	def set_tile_id(self, y, x, tile_id):
		self.tilefile[self.getloc(y, x)] = tile_id

	def get_tile_from_coord(self, y, x):
		return gettile(self.get_tile_id(y, x), self.tile_dict)

	def get_tile_from_loc(self, loc):
		return gettile(self.tilefile[loc], self.tile_dict)

	def tilemap(self):
		for key in self.tilefile:
			yield gettile(key, self.tile_dict)

	def add_monster_file(self, monster):
		self.monster_files.append(monster)

	def getloc(self, y, x):
		return y * self.cols + x
