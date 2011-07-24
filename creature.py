import curses
from random import randrange, randint, choice
from pio import io
from char import Char
from creature_stats import Stats


class Creature:
	"""This is an abstract class representing a creature"""

	def __init__(self):
		self.name = "creature"
		self.n = "him"
		self.char = Char('@', "white")
		self.stat = Stats()
		self.hp = self.stat.max_hp
		self.loc = None
