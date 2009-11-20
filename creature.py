import random
from char import Char
from colors import color

mons = ['k', '@', 'g', 'j', 'c']
name1 = ["kobold", "bandit", "goblin", "jelly", "centipede"]
name2 = ["black", "green", "yellow", "blue"]
name3 = ["him", "him", "him", "it", "it"]
color_ = [color["black"], color["light_green"], color["yellow"], color["blue"]]

class Creature:
	def __init__(self):
		i1, i2 = random.randrange(len(mons)), random.randrange(len(color_))
		self.name = name2[i2]+" "+name1[i1]
		self.ch = Char(mons[i1], color_[i2])
		self.n = name3[i1]
		self.sight = 8
		self.hp = 50

	def act(self, game):
		y,x = game.cur_level.squares[self].y, game.cur_level.squares[self].x
		loc = y + random.randrange(3)-1, x + random.randrange(3)-1
		self.move(loc, game.cur_level)

	def move(self, loc, level):
		dy, dx = loc #destination
		sy, sx = level.squares[self].y, level.squares[self].x #self
		ny, nx = None, None #square to move to
		if dy-sy > 0:
			ny = sy+1
		elif dy-sy < 0:
			ny = sy-1
		else:
			ny = sy

		if dx-sx > 0:
			nx = sx+1
		elif dx-sx < 0:
			nx = sx-1
		else:
			nx = sx

		target_square = level.getSquare(ny,nx)

		if target_square.passable():
			level.moveCreature(self, target_square)

	def loseHP(self, amount):
#		self.hp -= amount
#		if self.hp <= 0:
#			self.die
		pass

	def die(self):
		pass
