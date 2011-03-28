import random

from const.game import PASSAGE_UP, PASSAGE_DOWN, UP, DOWN, DUNGEON
from const.game import MAP_ROWS, MAP_COLS


class LevelTemplates(dict):
	"""A template for generated dungeons."""

	def __init__(self):
		dict.__init__(self)

		self.add_dungeon_template(DUNGEON)
		self.add_random_level_template(self[DUNGEON])
		self.add_random_level_template(self[DUNGEON])
		self.add_random_level_template(self[DUNGEON])
		self.add_random_level_template(self[DUNGEON])

	def add_dungeon_template(self, dungeon_key):
		self[dungeon_key] = {}

	def add_random_level_template(self, dungeon):
		i = len(dungeon)
		dungeon[i] = LevelTemplate(i)

	def add_predefined_level_template(self, dungeon, tilemap):
		i = len(dungeon)
		dungeon[i] = LevelTemplate(i, tilemap)


class LevelTemplate():

	def __init__(self, danger_level=0, tilemap=None):
		self.danger_level = danger_level
		self.tilemap = tilemap
		self.passages = {}

		if tilemap is not None:
			self.rows = tilemap.rows
			self.cols = tilemap.cols

			for key in tilemap.entrance_locs:
				if key == PASSAGE_UP:
					self.passages[key] = UP
				elif key == PASSAGE_DOWN:
					self.passages[key] = DOWN
				else:
					raise NotImplementedError
		else:
			self.passages = {PASSAGE_UP: UP, PASSAGE_DOWN: DOWN}
			self.rows = MAP_ROWS
			self.cols = MAP_COLS
