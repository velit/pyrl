import const.game as CG

from random import randrange


class Dice:
	"""An xDy dice object, has roll."""

	if CG.OPTIMIZATION:
		__slots__ = ("num", "sides", "addition")

	def __init__(self, num=1, sides=6, addition=0):
		self.num = num
		self.sides = sides
		self.addition = addition

	def roll(self):
		return sum(randrange(self.sides) + 1 for die in range(self.num)) + self.addition

	if CG.OPTIMIZATION:
		def __getstate__(self):
			return self.num, self.sides, self.addition

	if CG.OPTIMIZATION:
		def __setstate__(self, state):
			self.num, self.sides, self.addition = state

def dice_roll(num=1, sides=6, addition=0):
	return sum(randrange(sides) + 1 for die in range(num)) + addition
