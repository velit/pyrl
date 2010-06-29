import curses
import cPickle

from os import path

from level import Level
from player import Player
from io import io

class Game(object):
	def __init__(self, main):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""
		self.main = main

		self.turn_counter = 0

		self.l = [Level(self, 1)]
		self.p = Player(self, self.l[0])
		self.p.l.addCreature(self.p)
		self.redraw()
	
	def play(self):
		for creature in self.p.l.creatures:
			creature.act()
		self.turn_counter += 1

	def descend(self):
		self.p.l.removeCreature(self.p)
		if len(self.l) == self.l.index(self.p.l) + 1:
			self.p.l = Level(self, len(self.l)+1)
			self.p.l.addCreature(self.p, self.p.l.squares["us"])
			self.l.append(self.p.l)
		else:
			self.p.l = self.l[self.l.index(self.p.l) + 1]
			self.p.l.addCreature(self.p, self.p.l.squares["us"])
		self.redraw()

	def ascend(self):
		if self.l.index(self.p.l) > 0:
			self.p.l.removeCreature(self.p)
			self.p.l = self.l[self.l.index(self.p.l) - 1]
			self.p.l.addCreature(self.p, self.p.l.squares["ds"])
			self.redraw()
		else:
			self.endgame()
			
	def endgame(self, ask=True):
		if not ask:
			exit()
		io.queueMsg("Do you wish to end the game? [y/N]:")
		c = io.getCharacters(map(ord, ('y', 'Y', 'n', 'N', '\n', ' ')))
		if c in map(ord, ('y', 'Y')):
			exit()
	
	def _save(self):
		with open(path.join("data", "pyrl.svg"), "w") as f:
			cPickle.dump(self.p.l.map, f)

	def savegame(self, ask=True):
		if not ask:
			self._save()
			self.endgame(True)
		io.queueMsg("Do you wish to save the game? [Y/n]:")
		c = io.getCharacters(map(ord, ('y', 'Y', 'n', 'N', '\n', ' ')))
		if c in map(ord, ('y', 'Y', '\n', ' ')):
			self._save()
			self.endgame(True)

	def loadgame(self, ask=True):
		if not ask:
			self.main.load()
		io.msg("Do you wish to load the game? [y/N]:")
		c = io.getCharacters(map(ord, ('y', 'Y', 'n', 'N', '\n', ' ')))
		if c in map(ord, ('y', 'Y')):
			self.main.load()

	def redraw(self):
		self.p.l.drawMemory()
