import curses
import sys
import pickle

from level import Level
from player import Player
from io import IO
from fov import calcFov

class Game:
	def __init__(self, w):
		self.ydelta = 2 #two lines of room left for the interface in the top and bottom
		self.xdelta = 0
		self.dimensions = 20, 80#w.getmaxyx()[0]-self.ydelta*2, w.getmaxyx()[1]-self.xdelta*2
		IO().dy = self.ydelta

		self.turn_counter = 0

		self.player = Player()
		self.cur_level = Level(self.dimensions, 1)
		self.cur_level.addCreature(self.player)
		self.levels = [self.cur_level]
	
	def play(self):
		calcFov(self.player, self.cur_level)
		self.cur_level.draw()
		IO().drawInterface(self.turn_counter, self.cur_level.id)
		for creature in self.cur_level.creatures:
			creature.act(self)
		self.turn_counter += 1

	def descend(self):
		self.cur_level.removeCreature(self.player)
		if len(self.levels) == self.levels.index(self.cur_level) + 1:
			self.cur_level = Level(self.dimensions, len(self.levels)+1)
			self.cur_level.addCreature(self.player, self.cur_level.squares["us"])
			self.levels.append(self.cur_level)
		else:
			self.cur_level = self.levels[self.levels.index(self.cur_level) + 1]
			self.cur_level.addCreature(self.player, self.cur_level.squares["us"])
		self.cur_level.draw()

	def ascend(self):
		if self.levels.index(self.cur_level) > 0:
			self.cur_level.removeCreature(self.player)
			self.cur_level = self.levels[self.levels.index(self.cur_level) - 1]
			self.cur_level.addCreature(self.player, self.cur_level.squares["ds"])
			self.cur_level.draw()
		else:
			self.endGame()
			
	def endGame(self, dontAsk=False):
		if dontAsk:
			sys.exit(0)
		IO().printMsg("Do you wish to end the game? [y/N]:")
		c = IO().getCharacters([10,78,110,121])
		if c == 121:
			sys.exit(0)

	def saveGame(self, dontAsk=False):
		if dontAsk:
			pickle.dump(self, open("pyrl.svg", "w"))
			self.endGame(True)
		IO().printMsg("Do you wish to save the game? [Y/n]:")
		c = IO().getCharacters([10,78,110,121])
		if c in (121, 10):
			pickle.dump(self, open("pyrl.svg", "w"))
			self.endGame(True)

