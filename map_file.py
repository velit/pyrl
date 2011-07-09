from tiles import FLOOR, gettile
from const.game import MAP_ROWS, MAP_COLS

class MapFile:
	"""A map containing the tiles of a level."""

	def __init__(self, rows=MAP_ROWS, cols=MAP_COLS, tile=FLOOR):
		self.rows = rows
		self.cols = cols
		self.tilemap = [tile for i in range(rows * cols)]
		self.entrance_locs = {}
		self.tile_dict = {}

	def get_tile_id(self, y, x):
		return self.tilemap[y * self.cols + x]

	def set_tile_id(self, y, x, tile_id):
		self.tilemap[y * self.cols + x] = tile_id

	def gettile(self, y, x):
		return gettile(self.get_tile_id(y, x), self.tile_dict)

def GeneratedMapFile(rows=MAP_ROWS, cols=MAP_COLS):
	return (rows, cols)
