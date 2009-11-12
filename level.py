import random
import curses

from player import Player
from monster import Monster
from square import Square
from map import Map
from io import IO

class Level:
	def __init__(self, id):
		self.id = id
		self.rows, self.cols = IO().level_dimensions
		
		self.creatures = []

		self.map = Map(self.rows, self.cols)
		self.squares = self.map.squares

		for x in range(10):
			self.addCreature(Monster())

	def getSquare(self, y, x):
		return self.map.getSquare(y,x)
	
	def getFreeTile(self):
		return self.map.getFreeTile()

	def getRandomTile(self):
		return self.map.getRandomTile()

	def visitSquare(self, y, x):
		self.getSquare(y,x).visit()
	
	def seeThrough(self, y, x):
		return y >= 0 and x >= 0 and y < self.rows and x < self.cols and self.getSquare(y,x).seeThrough()

	def draw(self):
		IO().drawMap(self.map.map)

	def addCreature(self, creature, square = None):
		if square is None:
			square = self.getFreeTile()
		self.creatures.append(creature)
		square.creature = creature
		self.squares[creature] = square

	def moveCreature(self, creature, square):
		square.creature = creature
		self.squares[creature].creature = None
		self.squares[creature] = square

	def removeCreature(self, creature):
		square = self.squares[creature]
		self.creatures.remove(creature)
		self.squares[creature].creature = None
		del self.squares[creature]

	def getClosestInSquare(self, creature, radius):
		y, x = self.squares[creature].y, self.squares[creature].x
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
		y,x=self.squares[creature].y, self.squares[creature].x
		radius = min(self.rows-y, y, self.cols-x, x)
		for i in range(1, radius):
			c = self.getClosestInSquare(creature, i)
			if c:
				return c
		else:
			return False

	def getClosestCreature(self, target_creature):
		tcreature_square = self.squares[target_creature]
		ty, tx = tcreature_square.y, tcreature_square.x
		best, cre = None, None
		for creature in self.creatures:
			creature_square = self.squares[creature]
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
