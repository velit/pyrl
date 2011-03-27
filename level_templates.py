import random

from const.game import PASSAGE_UP, PASSAGE_DOWN, UP, DOWN, DUNGEON


class LevelTemplates(dict):
	"""A template for generated dungeons."""

	def __init__(self):
		dict.__init__(self)
		self.tilemaps = {}

		self.add_dungeon_template(DUNGEON)
		self.add_random_level_template(self[DUNGEON])

	def add_dungeon_template(self, dungeon_key):
		self[dungeon_key] = {}

	def add_random_level_template(self, dungeon):
		i = len(dungeon)
		dungeon[i] = LevelTemplate(i)

	def add_predefined_level_template(self, dungeon, tilemap_key):
		i = len(dungeon)

		passages = {}
		for key in self.tilemaps[tilemap_key].entrance_locs:
			if key == PASSAGE_UP:
				passages[key] = UP
			elif key == PASSAGE_DOWN:
				passages[key] = DOWN
			else:
				raise NotImplementedError

		dungeon[i] = LevelTemplate(i, tilemap_key, passages)


class LevelTemplate():

	def __init__(self, danger_level=0, tilemap_key=None, passages=None):
		self.danger_level = danger_level
		self.tilemap_key = tilemap_key
		if passages is None:
			self.passages = {PASSAGE_UP: UP, PASSAGE_DOWN: DOWN}
		else:
			self.passages = passages
