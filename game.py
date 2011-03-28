import os
import pickle

from pio import io
from player import Player
from level import Level
from world import World

from const.game import YES, NO, DEFAULT, DUNGEON
from const.game import DEBUG


class Game():

	def __init__(self):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""

		self.turn_counter = 0
		self.p = Player(self)
		self.world = World(self)

		self.world.change_level(DUNGEON)

	def enter_corresponding_level(self, *args, **kwords):
		return self.world.enter_corresponding_level(*args, **kwords)

	def play(self):
		for creature in self.p.l.creatures:
			creature.act()
		self.turn_counter += 1

	def endgame(self, ask=True):
		if not ask:
			exit()
		c = io.sel_getch("Do you wish to end the game? [y/N]:")
		if c in YES:
			exit()

	def _save(self):
		with open(os.path.join("data", "pyrl.svg"), "wb") as f:
			pickle.dump(self, f)

	def savegame(self, ask=True):
		if not ask:
			self._save()
			self.endgame(True)
		c = io.sel_getch("Do you wish to save the game? [Y/n]:")
		if c in YES | DEFAULT:
			self._save()
			self.endgame(True)

	def loadgame(self, ask=True):
		if not ask:
			self.main.load()
		c = io.sel_getch("Do you wish to load the game? [y/N]:")
		if c in YES:
			self.main.load()

	def redraw(self):
		self.p.redraw_view()
