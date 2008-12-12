from char import Char

class Floor:
	def __init__(self, name = "Undiscovered terrain", ch = Char(' '), \
			passable = False, destroyable = True):
		self.name = name
		self.ch = ch
		self.passable = passable
		self.destroyable = destroyable
