import pickle
import os

from pio import io
from level import Level
from player import Player
from const.game import YES, NO, DEFAULT, PASSAGE_DOWN, PASSAGE_UP
from const.game import SET_LEVEL, PREVIOUS_LEVEL, NEXT_LEVEL
from const.game import DEBUG

class Game(object):
	def __init__(self):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""

		self.turn_counter = 0
		self.dungeons = {}
		self.p = Player(self)

		with open(os.path.join("data", "data"), "rb") as f:
			data = pickle.load(f)

		if DEBUG:
			self.p.l = Level(self)
			self.p.l.addcreature(self.p)
		else:
			self.tilemaps = data.tilemaps
			self.dungeon_properties = data.dungeons
			self.change_level("wild", 0, PASSAGE_DOWN)

		self.redraw()

	def play(self):
		for creature in self.p.l.creatures:
			creature.act()
		self.turn_counter += 1

	def exit_level(self, world_loc, exit_point):
		passage_info = self.get_passages(*world_loc)[exit_point]
		if passage_info[0] == SET_LEVEL:
			self.change_level(*passage_info[1])
		elif passage_info[0] == PREVIOUS_LEVEL:
			dkey, i = self.level
			self.change_level(dkey, i-1, PASSAGE_DOWN)
		elif passage_info[0] == NEXT_LEVEL:
			dkey, i = self.level
			self.change_level(dkey, i+1, PASSAGE_UP)

	def get_level(self, dungeon_key, level_i):
		return self.dungeons[dungeon_key][level_i]

	def get_tilemap_handle(self, dungeon_key, level_i):
		return self.dungeon_properties[dungeon_key][level_i].tilemap_handle

	def get_passages(self, dungeon_key, level_i):
		return self.dungeon_properties[dungeon_key][level_i].passages

	def change_level(self, dkey, i, passage):
		if self.p.l is not None:
			self.p.l.removecreature(self.p)
		try:
			self.p.l = self.get_level(dkey, i)
		except KeyError:
			self.p.l = self.new_level(dkey, i)

		self.p.l.addcreature(self.p, self.p.l.getsquare(passage))
		self.level = (dkey, i)
		self.redraw()

	def new_level(self, dkey, i):
		if dkey not in self.dungeons:
			self.dungeons[dkey] = {}
		if i not in self.dungeons[dkey]:
			self.dungeons[dkey][i] = {}
		key = self.get_tilemap_handle(dkey, i)
		if key is not None:
			self.dungeons[dkey][i] = Level(self, dkey, i, self.tilemaps[key])
		else:
			self.dungeons[dkey][i] = Level(self, dkey, i,
					passages=self.get_passages(dkey, i))
		return self.dungeons[dkey][i]

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
