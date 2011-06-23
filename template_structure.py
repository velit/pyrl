import random

from char import Char
from templates import LevelTemplate, RDGTemplate, MonsterTemplate
from monster import mons
from const.game import DUNGEON


#class MonsterList(list):
#	def __init__(self, *args, **kwords):
#		super().__init__(*args, **kwords)

#	def add_monster_template(self, monster_template):
#		self.monsterlist.append(monster_template)

#	def get_level_monster_list(self, level_i):
#		level_monster_list = []
#		for mt in self:
#			start = mt.speciation_lvl
#			stop = mt.extinction_lvl
#			if start <= level_i:
#				weight_coeff = level_i + 10 - mt.speciation_lvl
#				level_monster_list.extend([mt]*weight_coeff)
#		return level_monster_list


class TemplateStructure:
	"""A template for dungeons."""

	def __init__(self):
		self.levels = {}
		self.monster_templates = []

		self.add_dungeon_template(DUNGEON)
		for x in range(20):
			self.add_random_level_template(self.levels[DUNGEON])
		self.getlvl(DUNGEON, 3).addmonster(MonsterTemplate("The Crone", 50, Char('@', "purple")))

		for m in mons:
			self.add_monster_template(m)

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

	def add_monster_template(self, monster_template):
		self.monster_templates.append(monster_template)

	def get_level_monster_list(self, level_i):
		level_monster_list = []
		for mt in self.monster_templates:
			start = mt.speciation_lvl
			stop = mt.extinction_lvl
			if start <= level_i:
				weight_coeff = level_i - mt.speciation_lvl
				level_monster_list.extend([mt]*weight_coeff)
		return level_monster_list
