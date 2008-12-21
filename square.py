from io import IO

class Square:
	def __init__(self, tile, y, x):
		self.loc = y, x
		self.floor = tile
		self.creature = None

	#returns true if the square is passable by creatures
	def passable(self):
		if self.creature is not None:
			return False
		elif self.floor is not None:
			return self.floor.passable
		else:
			return False

	#returns the visible character of the square
	def getChar(self):
		if self.creature is not None:
			return self.creature.ch.symbol
		else:
			return self.floor.ch.symbol

	def getColor(self):
		if self.creature is not None:
			return self.creature.ch.color
		else:
			return self.floor.ch.color

	def draw(self):
		IO().drawTile(self)
