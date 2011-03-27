import os
import pickle

from pio import io
from level import Level
from level_templates import LevelTemplates
from const.game import DUNGEON
from const.game import PASSAGE_UP, PASSAGE_DOWN, PASSAGE_RANDOM
from const.game import SET_LEVEL, PREVIOUS_LEVEL, NEXT_LEVEL


class World():

	def __init__(self, game):
		self.g = game
		self.levels = {}
		self.templates = None

		try:
			with open(os.path.join("data", "level_templates"), "rb") as f:
				self.templates = pickle.load(f)
		except IOError:
			io.a.sel_getch("Something went wrong with loading game files, "
					"resetting to default values.")
			self.templates = LevelTemplates()

	def enter_corresponding_level(self, world_loc, exit_point):
		d, i = world_loc
		passage_info = self.templates[d][i].passages[exit_point]
		if passage_info[0] == SET_LEVEL:
			self.change_level(*passage_info[1])
		elif passage_info[0] == PREVIOUS_LEVEL:
			self.change_level(d, i - 1, PASSAGE_DOWN)
		elif passage_info[0] == NEXT_LEVEL:
			self.change_level(d, i + 1, PASSAGE_UP)

	def change_level(self, dkey, level_i=0, passage=PASSAGE_RANDOM):
		p_l = self.g.p.l
		try:
			self.g.p.l = self.levels[dkey + str(level_i)]
		except KeyError:
			self.new_level(dkey, level_i)
			self.g.p.l = self.levels[dkey + str(level_i)]

		self.g.p.l.addcreature(self.g.p, self.g.p.l.getsquare(passage))
		if p_l is not None:
			p_l.removecreature(self.g.p)
		self.g.redraw()

	def new_level(self, d, i):
		tl = self.templates[d][i]
		if tl.tilemap_key is None:
			lvl = Level(self.g, d, i, passages=tl.passages)
		else:
			lvl = Level(self.g, d, i, self.templates.tilemaps[tl.tilemap_key])
		self.levels[d + str(i)] = lvl
