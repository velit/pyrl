import random

from templates import LevelTemplate, DungeonTemplate, RDGTemplate
from const.game import DUNGEON


class TemplateStructure(dict):
	"""A template for dungeons."""

	def __init__(self):
		dict.__init__(self)

		self.add_dungeon_template(DUNGEON)
		for x in range(4):
			self.add_random_level_template(self[DUNGEON])

	def add_dungeon_template(self, dungeon_key):
		self[dungeon_key] = DungeonTemplate()

	def add_random_level_template(self, dungeon):
		i = len(dungeon)
		dungeon[i] = LevelTemplate(i, RDGTemplate(), False)

	def add_predefined_level_template(self, dungeon, tilemap):
		i = len(dungeon)
		dungeon[i] = LevelTemplate(i, tilemap)
