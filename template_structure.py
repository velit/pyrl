import random

from char import Char
from templates import LevelTemplate, RDGTemplate, MonsterTemplate
from const.game import DUNGEON


class TemplateStructure():
	"""A template for dungeons."""

	def __init__(self):
		self.levels = {}

		self.add_dungeon_template(DUNGEON)
		for x in range(4):
			self.add_random_level_template(self.levels[DUNGEON])
		boss = MonsterTemplate("The Crone", 50, Char('@', "purple"))
		self.getlvl(DUNGEON, 3).addmonster(boss)

	def add_dungeon_template(self, dungeon_key):
		self.levels[dungeon_key] = {}

	def add_random_level_template(self, dungeon):
		i = len(dungeon)
		dungeon[i] = LevelTemplate(i, RDGTemplate(), False)

	def add_predefined_level_template(self, dungeon, tilemap):
		i = len(dungeon)
		dungeon[i] = LevelTemplate(i, tilemap)

	def getlvl(self, d, i):
		return self.levels[d][i]
