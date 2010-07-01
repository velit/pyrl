import random
import curses

import path

from player import Player
from monster import Monster
from square import Square
from tile import tiles
from io import io
from colors import color
from rdg import generateLevel, init_map

class Level(object):
	def __init__(self, game=None, id=None, generate=False):
		self.g = game
		self.id = id
		self.rows, self.cols = io.level_rows, io.level_cols
		
		self.creatures = []
		self.squares = {}

		if game and generate:
			generateLevel(self)
			for x in range(100):
				self.addCreature(Monster(self.g, self))
		else:
			self.map = init_map(self.rows, self.cols, tiles["f"])

	def getSquare(self, y, x):
		return self.map[y*self.cols + x]

	def getFreeTile(self):
		while True:
			tile = self.getRandomTile()
			if tile.passable():
				return tile

	def getRandomTile(self):
		return random.choice(self.map)

	def visitSquare(self, y, x):
		if self.legal_yx(y, x):
			self.getSquare(y,x).visit()
			return True
		return False

	def seeThrough(self, y, x):
		return self.legal_yx(y, x) and self.getSquare(y, x).seeThrough()

	def legal_yx(self, y, x):
		return 0 <= y < self.rows and 0 <= x < self.cols

	def draw(self):
		io.drawMap(self)
	
	def drawMemory(self):
		io.drawMemoryMap(self)

	def addCreature(self, creature, square = None):
		if square is None:
			square = self.getFreeTile()
		self.creatures.append(creature)
		square.creature = creature
		creature.square = square

	def moveCreature(self, creature=None, square=None, y=None, x=None):
		square.creature = creature
		creature.square.creature = None
		creature.square = square

	def removeCreature(self, creature):
		creature.square.creature = None
		self.creatures.remove(creature)

	def getClosestInSquare(self, creature, radius):
		y, x = self.square.y, self.square.x
		for i in range(radius*2):
			c = self.getSquare(y-radius, x-radius+i).creature
			if c: return c
			c = self.getSquare(y-radius+i, x+radius).creature
			if c: return c
			c = self.getSquare(y+radius, x+radius-i).creature
			if c: return c
			c = self.getSquare(y+radius-i, x-radius).creature
			if c: return c
		else:
			return False

	def getClosestCreatureFromArea(self, creature):
		y,x=self.square.y, self.square.x
		radius = min(self.rows-y, y, self.cols-x, x)
		for i in range(1, radius):
			c = self.getClosestInSquare(creature, i)
			if c:
				return c
		else:
			return False

	def getClosestCreature(self, target_creature):
		tcreature_square = target_creature.square
		ty, tx = tcreature_square.y, tcreature_square.x
		best, cre = None, None
		for creature in self.creatures:
			creature_square = creature.square
			y, x = creature_square.y, creature_square.x
			a = (ty-y) ** 2 + (tx-x) ** 2
			if a > 0:
				if best is None:
					best = a
					cre = creature
				elif a < best:
					best = a
					cre = creature
		return cre

	def check_los(self, startSquare, targetSquare):
		x0, y0 = startSquare.y, startSquare.x
		x1, y1 = targetSquare.y, targetSquare.x
		steep = abs(y1 - y0) > abs(x1 - x0)
		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1
		if x0 > x1:
			x0, x1 = x1, x0
			y0, y1 = y1, y0
		deltax = x1 - x0
		deltay = abs(y1 - y0)
		error = deltax / 2
		ystep = None
		y = y0
		if y0 < y1:
			ystep = 1
		else:
			ystep = -1
		for x in range(x0, x1):
			if steep:
				if not self.getSquare(y,x).seeThrough():
					return False
			else:
				if not self.getSquare(x,y).seeThrough():
					return False
			error -= deltay
			if error < 0:
				y += ystep
				error += deltax
		else:
			return True

	def neighbor_nodes(self, y, x):
		for j in range(y-1, y+2):
			for i in range(x-1, x+2):
				if not ((y == j and x == i) and self.legal_yx(y, x) and
						self.getSquare(j, i).tile_passable()):
					yield self.getSquare(j, i)

	def path(self, start, goal):
		return path.path(start, goal, self)
