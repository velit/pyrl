import os
import pickle

from pio import io
from player import Player
from level import Level
from input_interpretation import get_input_and_act
from world_file import WorldFile
from const.game import DEBUG, YES
from const.game import DUNGEON, FIRST_LEVEL
from const.game import SET_LEVEL, PREVIOUS_LEVEL, NEXT_LEVEL
from const.game import PASSAGE_UP, PASSAGE_DOWN


class Game:

	def __init__(self, main):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""

		self.main = main
		self.turn_counter = 0

		self.levels = {}
		self.world_file = WorldFile()
		self.player = Player(self)
		self.init_new_level(FIRST_LEVEL)
		self.cur_level = self.levels[FIRST_LEVEL]
		self.cur_level.addcreature(self.player)
	
	def enter_passage(self, origin_world_loc, origin_passage):
		instruction, d, i = self.world_file.get_passage_info(origin_world_loc, origin_passage)
		if instruction == SET_LEVEL:
			self.change_level((d, i))
		else:
			d, i = self.cur_level.world_loc
			if instruction == PREVIOUS_LEVEL:
				self.change_level((d, i - 1), PASSAGE_DOWN)
			elif instruction == NEXT_LEVEL:
				self.change_level((d, i + 1), PASSAGE_UP)

	def change_level(self, world_loc, passage):
		self.cur_level.removecreature(self.player)
		try:
			self.cur_level = self.levels[world_loc]
		except KeyError:
			self.init_new_level(world_loc)
			self.cur_level = self.levels[world_loc]
		self.cur_level.addcreature(self.player, self.cur_level.get_passage_loc(passage))
		self.redraw()

	def init_new_level(self, world_loc):
		level_file = self.world_file.get_level_file(*world_loc)
		danger_level = level_file.danger_level
		level_monster_list = self.world_file.get_level_monster_list(danger_level)
		self.levels[world_loc] = Level(self, world_loc, level_file, level_monster_list)

	def play(self):
		creature = self.cur_level.turn_scheduler.get()
		if creature == self.player:
			creature.update_view()
			get_input_and_act(self)
		self.turn_counter += 1

	def endgame(self, ask=True):
		if not ask:
			exit()
		if io.sel_getch("Do you wish to end the game? [y/N]") in YES:
			exit()

	def _save(self):
		with open(os.path.join("data", "pyrl.svg"), "wb") as f:
			pickle.dump(self, f)

	def savegame(self, ask=True):
		if not ask:
			self._save()
			self.endgame(False)
		elif io.sel_getch("Do you wish to save the game? [y/N]") in YES:
			self._save()
			self.endgame(True)

	def loadgame(self, ask=True):
		if not ask:
			self.main.load()
		if io.sel_getch("Do you wish to load the game? [y/N]") in YES:
			self.main.load()

	def redraw(self):
		self.player.redraw_view()
