import const.game as GAME
import const.colors as COLOR

from char import Char
from level_file import LevelFile
from monster_file import MonsterFile, monster_files

class WorldFile(object):

	def __init__(self):
		self.level_files = {}
		self.level_passageways = {}
		self.dungeon_lengths = {}
		self.global_monster_files = []

		self.add_dungeon(GAME.DUNGEON)
		for x in xrange(GAME.LEVELS_PER_DUNGEON):
			self.add_level_file(GAME.DUNGEON)
		d0 = self.get_level_file((GAME.DUNGEON, 0))
		d0.add_monster_file(MonsterFile("The Crone", Char('@', COLOR.PURPLE)))

		for m in monster_files:
			self.add_monster_file(m)

	def add_monster_file(self, monster_file):
		self.global_monster_files.append(monster_file)

	def add_dungeon(self, dungeon_key):
		self.dungeon_lengths[dungeon_key] = 0

	def add_level_file(self, dungeon_key):
		level_i = self.dungeon_lengths[dungeon_key]
		self.level_files[dungeon_key, level_i] = LevelFile(level_i)
		self.level_passageways[dungeon_key, level_i] = {GAME.PASSAGE_UP: GAME.UP, GAME.PASSAGE_DOWN: GAME.DOWN}
		self.dungeon_lengths[dungeon_key] += 1

	def get_level_file(self, world_loc):
		try:
			return self.level_files[world_loc]
		except KeyError:
			raise GAME.PyrlException("Nonexistant level key: {}".format(world_loc))

	def pop_level_file(self, world_loc):
		try:
			level_file = self.level_files[world_loc]
		except KeyError:
			raise GAME.PyrlException("Nonexistant level key: {}".format(world_loc))
		else:
			del self.level_files[world_loc]
			return level_file

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
