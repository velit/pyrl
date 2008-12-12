from creature import Creature
from io import IO
from char import Char

class Monster(Creature):
	def __init__(self):
		self.ch = Char('k', IO().colors["light_green"])
