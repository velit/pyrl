import curses
import sys
import cPickle

from level import Level
from player import Player
from io import io

class Game:
	def __init__(self):
		"""The game object for Tapani Kiiskisen's game pyrl made with curses."""
		self.turn_counter = 0

		self.player = Player(self)
		self.cur_level = Level(1)
		self.cur_level.addCreature(self.player)
		self.levels = [self.cur_level]
	
	def play(self):
		for creature in self.cur_level.creatures:
			creature.act(self)
		self.turn_counter += 1

	def descend(self):
		self.cur_level.removeCreature(self.player)
		if len(self.levels) == self.levels.index(self.cur_level) + 1:
			self.cur_level = Level(len(self.levels)+1)
			self.cur_level.addCreature(self.player, self.cur_level.squares["us"])
			self.levels.append(self.cur_level)
		else:
			self.cur_level = self.levels[self.levels.index(self.cur_level) + 1]
			self.cur_level.addCreature(self.player, self.cur_level.squares["us"])
		self.cur_level.drawMemory()

	def ascend(self):
		if self.levels.index(self.cur_level) > 0:
			io.clearLos()
			self.cur_level.removeCreature(self.player)
			self.cur_level = self.levels[self.levels.index(self.cur_level) - 1]
			self.cur_level.addCreature(self.player, self.cur_level.squares["ds"])
			self.cur_level.drawMemory()
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
		cPickle.dump(self, f, "w")
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

