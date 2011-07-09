import os
import pickle

from pio import io
from player import Player
from level import Level
from input_interpretation import get_input_and_act
from world_file import WorldFile
from const.game import DEBUG, YES
from const.game import DUNGEON
from const.game import SET_LEVEL, PREVIOUS_LEVEL, NEXT_LEVEL
from const.game import PASSAGE_UP, PASSAGE_DOWN, PASSAGE_RANDOM


class Game:

	def __init__(self, main):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""

		self.main = main
		self.turn_counter = 0

		self.levels = {}
		self.world_file = WorldFile()
		self.player = Player(self)
		self.cur_level = None
		self.change_level(DUNGEON)
	
	def enter_passage(self, level, square):
		passage_info = level.passages[square.getexit()]
		d, i = self.cur_level.world_loc
		if passage_info[0] == SET_LEVEL:
			self.change_level(*passage_info[1])
		elif passage_info[0] == PREVIOUS_LEVEL:
			self.change_level(d, i - 1, PASSAGE_DOWN)
		elif passage_info[0] == NEXT_LEVEL:
			self.change_level(d, i + 1, PASSAGE_UP)

	def change_level(self, dkey, level_i=0, passage=PASSAGE_RANDOM):
		old_level = self.cur_level
		try:
			self.cur_level = self.levels[dkey + str(level_i)]
		except KeyError:
			self.init_new_level(dkey, level_i)
			self.cur_level = self.levels[dkey + str(level_i)]

		self.cur_level.addcreature(self.player, self.cur_level.getsquare(entrance=passage))
		if old_level is not None:
			old_level.removecreature(self.player)
		self.redraw()

	def init_new_level(self, d, i):
		f = self.world_file
		self.levels[d + str(i)] = Level(self, (d, i), f.get_level_file(d, i), f.get_level_monster_list(i))

	def play(self):
		for creature in self.cur_level.creatures:
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
