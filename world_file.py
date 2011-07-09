from char import Char
from const.game import DUNGEON
from level_file import LevelFile
from map_file import GeneratedMapFile
from monster_file import MonsterFile, monster_files

class WorldFile:
	"""A file which World can use to make real world."""

	def __init__(self):
		self.level_files = {}
		self.monster_files = []

		self.add_dungeon_file(DUNGEON)
		for x in range(20):
			self.add_random_level_file(self.level_files[DUNGEON])
		self.get_level_file(DUNGEON, 3).addmonster(MonsterFile("The Crone", 50, Char('@', "purple")))

		for m in monster_files:
			self.add_monster_file(m)

	def add_dungeon_file(self, dungeon_key):
		self.level_files[dungeon_key] = {}

	def add_random_level_file(self, dungeon):
		i = len(dungeon)
		dungeon[i] = LevelFile(i, GeneratedMapFile(), False)

	def add_predefined_level_file(self, dungeon, tilemap):
		i = len(dungeon)
		dungeon[i] = LevelFile(i, tilemap)

	def get_level_file(self, d, i):
		return self.level_files[d][i]

	def add_monster_file(self, monster_file):
		self.monster_files.append(monster_file)

	def get_level_monster_list(self, level_i):
		level_monster_list = []
		for mt in self.monster_files:
			start = mt.speciation_lvl
			stop = mt.extinction_lvl
			if start <= level_i:
				weight_coeff = level_i - mt.speciation_lvl
				level_monster_list.extend([mt]*weight_coeff)
		return level_monster_list
