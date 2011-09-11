import const.game as GAME

from tiles import gettile

class LevelFile:

	def __init__(self, danger_level=0, rows=GAME.LEVEL_ROWS, cols=GAME.LEVEL_COLS):
		self.rows = rows
		self.cols = cols
		self.danger_level = danger_level
		self.passage_locations = {}
		self.monster_files = []
		self.tilefile = None
		self.tile_dict = {}

	def get_tile_id(self, y, x):
		return self.tilefile[self.getloc(y, x)]

	def set_tile_id(self, y, x, tile_id):
		self.tilefile[self.getloc(y, x)] = tile_id

	def get_tile_from_coord(self, y, x):
		return gettile(self.get_tile_id(y, x), self.tile_dict)

	def get_tile_fromloc(self, loc):
		return gettile(self.tilefile[loc], self.tile_dict)

	def get_tilemap(self):
		return [gettile(key, self.tile_dict) for key in self.tilefile]

	def add_monster_file(self, monster):
		self.monster_files.append(monster)

	def getloc(self, y, x):
		return y * self.cols + x
