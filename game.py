import os
import pickle

from pio import io
from player import Player
from level import Level
from template_structure import TemplateStructure

from const.game import DEBUG
from const.game import YES, DUNGEON, PASSAGE_RANDOM


class Game():

	def __init__(self):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""

		self.turn_counter = 0
		self.p = Player(self)
		self.levels = {}
		self.templs = None

		try:
			with open(os.path.join("data", "data"), "rb") as f:
				self.templs = pickle.load(f)
		except IOError as exc:
			io.msg("{}, resetting data to default values.".format(exc))
			self.templs = TemplateStructure()

		self.change_level(DUNGEON)

	def change_level(self, dkey, level_i=0, passage=PASSAGE_RANDOM):
		old_level = self.p.l
		try:
			self.p.l = self.levels[dkey + str(level_i)]
		except KeyError:
			self.init_new_level(dkey, level_i)
			self.p.l = self.levels[dkey + str(level_i)]

		self.p.l.addcreature(self.p, self.p.l.getsquare(entrance=passage))
		if old_level is not None:
			old_level.removecreature(self.p)
		self.redraw()

	def init_new_level(self, d, i):
		self.levels[d + str(i)] = Level(self, (d, i), self.templs.getlvl(d, i))

	def play(self):
		for creature in self.p.l.creatures:
			creature.act()
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
			self.endgame(True)
		if io.sel_getch("Do you wish to save the game? [y/N]") in YES:
			self._save()
			self.endgame(True)

	def loadgame(self, ask=True):
		if not ask:
			self.main.load()
		if io.sel_getch("Do you wish to load the game? [y/N]") in YES:
			self.main.load()

	def redraw(self):
		self.p.redraw_view()
