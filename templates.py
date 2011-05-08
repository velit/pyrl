from tiles import gettile, FLOOR
from const.game import MAP_ROWS, MAP_COLS, UP, DOWN, PASSAGE_UP, PASSAGE_DOWN
from char import Char

class MapTemplate():
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


class LevelTemplate():

	def __init__(self, danger_level=0, template=None, map_not_rdg=True):
		self.danger_level = danger_level
		self.passages = {}
		self.map_not_rdg = map_not_rdg #true: map, false: rdg
		self.template = template
		self.monsters = []

		if map_not_rdg:
			for key in template.entrance_locs:
				if key == PASSAGE_UP:
					self.passages[key] = UP
				elif key == PASSAGE_DOWN:
					self.passages[key] = DOWN
				else:
					raise NotImplementedError
		else:
			self.passages = {PASSAGE_UP: UP, PASSAGE_DOWN: DOWN}

	def addmonster(self, monster):
		self.monsters.append(monster)


def RDGTemplate(rows=MAP_ROWS, cols=MAP_COLS):
	return (rows, cols)


class MonsterTemplate():
	def __init__(self, name="kobold", base_hp=10, ch=Char('k', "green")):
		self.name = name
		self.base_hp = base_hp
		self.ch = ch
