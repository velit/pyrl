from random import randrange

class Creature:
	"""This is an abstract class representing a creature"""
	def __init__(self, level):
		self.sight = 8
		self.hp = 50
		self.l = level

	def act(self):
		y,x = self.l.squares[self].y, self.l.squares[self].x
		loc = y + randrange(3)-1, x + randrange(3)-1
		self.move(loc)

	def move(self, loc):
		dy, dx = loc #destination
		sy, sx = self.l.squares[self].y, self.l.squares[self].x #self
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

		target_square = self.l.getSquare(ny,nx)

		if target_square.passable():
			self.l.moveCreature(self, target_square)

	def loseHP(self, amount):
		self.hp -= amount
		if self.hp <= 0:
			self.die

	def die(self):
		self.l.removeCreature(self)
