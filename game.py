import curses
import sys
import pickle

from level import Level
from player import Player
from io import io

class Game:
	def __init__(self):
		"""The game object for Tapani Kiiskisen's game pyrl made with curses."""
		self.turn_counter = 0

		self.l = [Level(1)]
		self.p = Player(self.l[0], self)
		self.p.l.addCreature(self.p)
	
	def play(self):
		for creature in self.p.l.creatures:
			creature.act()
		self.turn_counter += 1

	def descend(self):
		self.p.l.removeCreature(self.p)
		if len(self.l) == self.l.index(self.p.l) + 1:
			self.p.l = Level(len(self.l)+1)
			self.p.l.addCreature(self.p, self.p.l.squares["us"])
			self.l.append(self.p.l)
		else:
			self.p.l = self.l[self.l.index(self.p.l) + 1]
			self.p.l.addCreature(self.p, self.p.l.squares["us"])
		self.p.l.drawMemory()

	def ascend(self):
		if self.l.index(self.p.l) > 0:
			self.p.l.removeCreature(self.p)
			self.p.l = self.l[self.l.index(self.p.l) - 1]
			self.p.l.addCreature(self.p, self.p.l.squares["ds"])
			self.p.l.drawMemory()
		else:
			self.endGame()
			
	def endGame(self, ask=True):
		if not ask:
			sys.exit(0)
		io.queueMsg("Do you wish to end the game? [y/N]:")
		c = io.getCharacters(map(ord, ('y', 'Y', 'n', 'N', '\n', ' ')))
		if c in map(ord, ('y', 'Y')):
			sys.exit(0)
	
	def _save(self):
		f = open("pyrl.svg", "w")
		pickle.dump(self, f)
		f.close()

	def saveGame(self, ask=True):
		if not ask:
			self._save()
			self.endGame(True)
		io.queueMsg("Do you wish to save the game? [Y/n]:")
		c = io.getCharacters(map(ord, ('y', 'Y', 'n', 'N', '\n', ' ')))
		if c in map(ord, ('y', 'Y')):
			self._save()
			self.endGame(True)

