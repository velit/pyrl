import random
import curses


from player import Player
from monster import Monster
from square import Square
from tile import tiles
from io import io
from rdg import generateLevel

class Level(object):
	def __init__(self, game, id, generate=True):
		self.g = game
		self.id = id
		self.rows, self.cols = io.level_rows, io.level_cols
		
		self.creatures = []
		self.squares = {}

		if generate:
			generateLevel(self)
		else:
			self.map = [[Square(tiles["f"],j,i) for i in range(self.cols)] for j in range(self.rows)]
			for x in range(self.cols):
				self.map[0][x].tile = tiles["w"]
				self.map[-1][x].tile = tiles["w"]
			for y in range(self.rows):
				self.map[y][0].tile = tiles["w"]
				self.map[y][-1].tile = tiles["w"]

		for x in range(10):
			self.addCreature(Monster(self.g, self))

	def getSquare(self, y, x):
		return self.map[y][x]

	def getFreeTile(self):
		while True:
			tile = self.getRandomTile()
			if tile.passable():
				return tile

	def getRandomTile(self):
		return random.choice(random.choice(self.map))

	def visitSquare(self, y, x):
		self.getSquare(y,x).visit()
	
	def seeThrough(self, y, x):
		return y >= 0 and x >= 0 and y < self.rows and x < self.cols and self.getSquare(y,x).seeThrough()

	def draw(self):
		io.drawMap(self.map.map)
	
	def drawMemory(self):
		io.drawMemoryMap(self.map)

	def addCreature(self, creature, square = None):
		if square is None:
			square = self.getFreeTile()
		self.creatures.append(creature)
		square.creature = creature
		creature.square = square

	def moveCreature(self, creature, square):
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
