import random
from char import Char
from io import IO

mons = ['k', '@', 'g', 'j', 'c']
name1 = ["kobold", "bandit", "goblin", "jelly", "centipede"]
color = [IO().colors["black"], IO().colors["light_green"], IO().colors["yellow"], IO().colors["blue"]] 
name2 = ["black", "green", "yellow", "blue"]
name3 = ["him", "him", "him", "it", "it"]

class Creature:
	def __init__(self):
		i1, i2 = random.randrange(len(mons)), random.randrange(len(color))
		self.name = name2[i2]+" "+name1[i1]
		self.ch = Char(mons[i1], color[i2])
		self.n = name3[i1]
		self.sight = 8
		self.hp = 50

	def act(self, game):
		#self.move(game.cur_level.squares[game.player].loc, game.cur_level)
		y,x = game.cur_level.squares[self].loc
		loc = y + random.randrange(3)-1, x + random.randrange(3)-1
		self.move(loc, game.cur_level)

	def move(self, loc, level):
		dy, dx = loc
		sy, sx = level.squares[self].loc #self loc
		ny, nx = None, None #newy
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

	def die(self):
		pass
