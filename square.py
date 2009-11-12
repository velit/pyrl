from tile import tiles
from io import IO

class Square:
	def __init__(self, tile, y, x):
		self.y = y
		self.x = x
		self.tile = tile
		self.creature = None
		self.memory_tile = tiles["u"]

	#returns true if the square is passable by creatures
	def passable(self):
		if self.creature is not None:
			return False
		elif self.tile is not None:
			return self.tile.passable
		else:
			return False

	def seeThrough(self):
		return self.tile.see_through

	def visit(self):
		self.memory_tile = self.tile
		IO().visibility.append(self)

	def getChar(self, memory=True):
		if memory and self.creature is not None:
			return (self.creature.ch.symbol, self.creature.ch.color)
		else:
			return (self.memory_tile.ch.symbol, self.memory_tile.ch.color)

	def getSymbol(self, memory=True):
		if memory and self.creature is not None:
			return self.creature.ch.symbol
		else:
			return self.memory_tile.ch.symbol

	def getColor(self, memory=True):
		if memory and self.creature is not None:
			return self.creature.ch.color
		else:
			return self.memory_tile.ch.color

	def draw(self):
		IO().drawTile(self)
