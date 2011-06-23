from random import randrange
from const.game import OPTIMIZATION


class Dice:
	"""An xDy dice object, has roll."""

	if OPTIMIZATION:
		__slots__ = ("num", "sides")

	def __init__(self, num=1, sides=6, addition=0):
		self.num = num
		self.sides = sides
		self.addition = addition

	def roll(self):
		return sum(randrange(self.sides) + 1 for die in range(self.num)) + addition

	if OPTIMIZATION:
		def __getstate__(self):
			return self.num, self.sides

	if OPTIMIZATION:
		def __setstate__(self, state):
			self.num, self.sides = state

def roll(num=1, sides=6, addition=0):
	return sum(randrange(sides) + 1 for die in range(num)) + addition
