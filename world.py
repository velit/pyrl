from player import Player
from level import Level
from const.game import PASSAGE_RANDOM


class World:
	def __init__(self, game, world_file):
		self.levels = {}
		self.world_file = world_file
		self.player = Player(game)
		self.cur_level = None

	def change_level(self, dkey, level_i=0, passage=PASSAGE_RANDOM):
		old_level = self.cur_level
		try:
			self.cur_level = self.levels[dkey + str(level_i)]
		except KeyError:
			self.init_new_level(dkey, level_i)
			self.cur_level = self.levels[dkey + str(level_i)]

		self.cur_level.addcreature(self.player, self.cur_level.getsquare(entrance=passage))
		if old_level is not None:
			old_level.removecreature(self.p)
		self.redraw()

	def init_new_level(self, d, i):
		f = self.world_file
		self.levels[d + str(i)] = Level(self, (d, i), f.get_level_file(d, i), f.get_level_monster_list(i))
