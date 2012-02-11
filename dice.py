import const.game as GAME

from random import randrange


class Dice(object):
	u"""An xDy dice object, has roll."""

	if GAME.OPTIMIZATION:
		__slots__ = (u"num", u"sides", u"addition")

	def __init__(self, num=1, sides=6, addition=0):
		self.num = num
		self.sides = sides
		self.addition = addition

	def roll(self):
		return sum(randrange(self.sides) + 1 for die in xrange(self.num)) + self.addition

	if GAME.OPTIMIZATION:
		def __getstate__(self):
			return self.num, self.sides, self.addition

	if GAME.OPTIMIZATION:
		def __setstate__(self, state):
			self.num, self.sides, self.addition = state

def dice_roll(num=1, sides=6, addition=0):
	return sum(randrange(sides) + 1 for die in xrange(num)) + addition
