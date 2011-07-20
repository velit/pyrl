from char import Char
from level_file import LevelFile
from monster_file import MonsterFile, monster_files
from const.game import DUNGEON, UP, DOWN, PASSAGE_UP, PASSAGE_DOWN

class WorldFile:
	"""A file which World can use to make real world."""

	def __init__(self):
		self.level_files = {}
		self.level_passageways = {}
		self.global_monster_files = []

		self.add_dungeon(DUNGEON)
		for x in range(20):
			self.add_level_file(DUNGEON)
		d3 = self.get_level_file(DUNGEON, 3)
		d3.add_monster_file(MonsterFile("The Crone", 50, Char('@', "purple")))

		for m in monster_files:
			self.add_monster_file(m)

	def add_monster_file(self, monster_file):
		self.global_monster_files.append(monster_file)

	def add_dungeon(self, dungeon_key):
		self.level_files[dungeon_key] = []

	def add_level_file(self, dungeon_key):
		dungeon = self.level_files[dungeon_key]
		level = LevelFile(len(dungeon))
		dungeon.append(level)
		level_i = dungeon.index(level)
		self.level_passageways[dungeon_key, level_i] = {PASSAGE_UP: UP, PASSAGE_DOWN: DOWN}

	def get_level_file(self, d, i):
		return self.level_files[d][i]

	def get_passage_info(self, world_loc, passage):
		return self.level_passageways[world_loc][passage]

	def get_level_monster_list(self, danger_level):
		level_monster_list = []
		for mt in self.global_monster_files:
			start = mt.speciation_lvl
			stop = mt.extinction_lvl
			if start <= danger_level:
				weight_coeff = danger_level - mt.speciation_lvl
				level_monster_list.extend([mt]*weight_coeff)
		return level_monster_list
