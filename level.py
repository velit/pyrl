import random
import curses

from player import Player
from monster import Monster
from square import Square
from map import Map
from io import IO

class Level:
	def __init__(self, dimensions, id):
		self.id = id
		self.dimensions = dimensions
		
		self.creatures = []
		self.squares = {}

		self.map = Map(self.dimensions, self.squares)

		for x in range(10):
			self.addCreature(Monster())

	def getSquare(self, y, x):
		return self.map.getSquare(y,x)
	
	def getFreeTile(self):
		return self.map.getFreeTile()

	def getRandomTile(self):
		return self.map.getRandomTile()

	def lightSquare(self, y, x):
		self.getSquare(y,x).flag = IO().flag
	
	def isLit(self, y, x):
		return self.getSquare(y,x).flag == IO().flag

	def seeThrough(self, y, x):
		rows, cols = self.dimensions
		return y >= 0 and x >= 0 and y < rows and x < cols and self.getSquare(y,x).seeThrough()

	def draw(self):
		self.map.draw()

	def addCreature(self, creature, square = None):
		if square is None:
			square = self.getFreeTile()
		self.creatures.append(creature)
		square.creature = creature
		self.squares[creature] = square
		#square.draw()

	def moveCreature(self, creature, square):
		square.creature = creature
		self.squares[creature].creature = None
		#self.squares[creature].draw()
		self.squares[creature] = square
		#square.draw()

	def removeCreature(self, creature):
		square = self.squares[creature]
		self.creatures.remove(creature)
		self.squares[creature].creature = None
		del self.squares[creature]
		#square.draw()

	def getClosestInSquare(self, creature, radius):
		y, x = self.squares[creature].loc
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
		y,x=self.squares[creature].loc
		radius = min(self.dimensions[0]-y, y, self.dimensions[1]-x, x)
		for i in range(1, radius):
			c = self.getClosestInSquare(creature, i)
			if c:
				return c
		else:
			return False

	def getClosestCreature(self, targetCreature):
		squaredDistance = 0
		for x in self.creatures:
			if squaredDistance == 0:
				pass
