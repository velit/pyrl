import curses
import cPickle as pickle

from os import path

from level import Level
from player import Player
from io import io
from constants import YES, NO, DEFAULT

#from dummy_map import DummyMap

class Game(object):
	def __init__(self, main):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""
		self.main = main

		#a = DummyMap(80, 50)
		#with open("temp", "w") as f:
		#	pickle.dump(a, f)

		self.turn_counter = 0

		self.l = [Level(self, 1)]
		self.p = Player(self, self.l[0])
		self.p.l.addcreature(self.p)
		self.redraw()
	
	def play(self):
		for creature in self.p.l.creatures:
			creature.act()
		self.turn_counter += 1

	def descend(self):
		self.p.l.removecreature(self.p)
		if len(self.l) == self.l.index(self.p.l) + 1:
			self.p.l = Level(self, len(self.l)+1)
			self.p.l.addcreature(self.p, self.p.l.getsquare("us"))
			self.l.append(self.p.l)
		else:
			self.p.l = self.l[self.l.index(self.p.l) + 1]
			self.p.l.addcreature(self.p, self.p.l.getsquare("us"))
		self.redraw()

	def ascend(self):
		if self.l.index(self.p.l) > 0:
			self.p.l.removecreature(self.p)
			self.p.l = self.l[self.l.index(self.p.l) - 1]
			self.p.l.addcreature(self.p, self.p.l.getsquare("ds"))
			self.redraw()
		else:
			self.endgame()
			
	def endgame(self, ask=True):
		if not ask:
			exit()
		c = io.getch_from_list(str="Do you wish to end the game? [y/N]:")
		if c in YES:
			exit()
	
	def _save(self):
		with open(path.join("data", "pyrl.svg"), "w") as f:
			pickle.dump(self, f)

	def savegame(self, ask=True):
		if not ask:
			self._save()
			self.endgame(True)
		c = io.getch_from_list(str="Do you wish to save the game? [Y/n]:")
		if c in YES | DEFAULT:
			self._save()
			self.endgame(True)

	def loadgame(self, ask=True):
		if not ask:
			self.main.load()
		c = io.getch_from_list(str="Do you wish to load the game? [y/N]:")
		if c in YES:
			self.main.load()

	def redraw(self):
		self.p.visibility.clear()
		self.p.l.drawmemory()
		self.p.update_los()
