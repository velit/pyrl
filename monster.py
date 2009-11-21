from char import Char
from creature import Creature
from random import choice
from colors import color

mons = (('k', "kobold", "him"), ('@', "bandit", "him"), ('g', "goblin", "him"), ('j', "jelly", "it"), ('c', "centipede", "it"))
col = (("black", color["black"]), ("green", color["light_green"]), ("yellow", color["yellow"]), ("blue", color["blue"]))

class Monster(Creature):
	def __init__(self, level):
		Creature.__init__(self, level)
		m = choice(mons)
		c = choice(col)
		self.name = c[0] + " " + m[1]
		self.ch = Char(m[0], c[1])
		self.n = m[2]
