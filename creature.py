import curses
from random import randrange
from io import io

# Multipliers for transforming coordinates to other octants:
mult = [[1,  0,  0, -1, -1,  0,  0,  1],
		[0,  1, -1,  0,  0, -1,  1,  0],
		[0,  1,  1,  0,  0, -1, -1,  0],
		[1,  0,  0,  1, -1,  0,  0, -1]]

class Creature(object):
	"""This is an abstract class representing a creature"""
	def __init__(self, game, level):
		self.sight = 6
		self.hp = 10
		self.dmg = 2
		self.g = game
		self.l = level
		self.square = None
		self.visibility = []

	def act(self):
		self.move(self.square.y + randrange(3) - 1, self.square.x + randrange(3) - 1)

	def getloc(self):
		return self.square.y, self.square.x

	def move(self, dy, dx):
		sy, sx = self.square.y, self.square.x #self
		ty, tx = sy, sx #square to move to
		if dy > sy:
			ty += 1
		if dy < sy:
			ty -= 1

		if dx > sx:
			tx += 1
		elif dx < sx:
			tx -= 1

		target_square = self.l.getSquare(ty,tx)

		if target_square.passable():
			self.l.moveCreature(self, target_square)
		elif target_square.creature is self.g.p:
			self.hit(target_square.creature)

	def loseHP(self, amount):
		self.hp -= amount
		if self.hp <= 0:
			self.die()

	def die(self):
		io.msg("The "+self.name+" dies.")
		self.l.removeCreature(self)

	def hit(self, creature):
		if creature is self.g.p:
			io.msg("The "+self.name+" hits the you for "+str(self.dmg)+" damage.")
		else:
			io.msg("The "+self.name+" hits the "+creature.name+" for "+str(self.dmg)+" damage.")
		creature.loseHP(self.dmg)

	def visitSquare(self, y, x):
		self.l.visitSquare(y,x)
		self.visibility.append((y,x))

	def has_los(self, target):
		sy, sx = self.getloc()
		py, px = target.getloc()
		if (sy - py) ** 2 + (sx - px) ** 2 <= (self.sight - 1) ** 2:
			return self.l.check_los(self.square, target.square)

	def updateLos(self):
		io.clearLos(self.visibility, self.l)
		y,x = self.square.y, self.square.x
		if self.sight > 0:
			self.visitSquare(y,x)
		for oct in range(8):
			self._cast_light(self.l, y, x, 1, 1.0, 0.0, self.sight, mult[0][oct], mult[1][oct], mult[2][oct], mult[3][oct])
		io.drawLos(self.visibility, self.l)

	# Algorithm by Bjorn Bergstrom bjorn.bergstrom@roguelikedevelopment.org Copyright 2001 
	# http://roguebasin.roguelikedevelopment.org/index.php?title=FOV_using_recursive_shadowcasting
	def _cast_light(self, level, cy, cx, row, start, end, radius, xx, xy, yx, yy):
		"Recursive lightcasting function"
		if start < end:
			return
		radius_squared = radius*radius
		for j in range(row, radius+1):
			dx, dy = -j-1, -j
			blocked = False
			while dx <= 0:
				dx += 1
				# Translate the dx, dy coordinates into map coordinates:
				X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
				# l_slope and r_slope store the slopes of the left and right
				# extremities of the square we're considering:
				l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
				if start < r_slope:
					continue
				elif end > l_slope:
					break
				else:
					# Our light beam is touching this square; light it:
					if dx*dx + dy*dy < radius_squared:
						self.visitSquare(Y, X)
					if blocked:
						# we're scanning a row of blocked squares:
						if not level.seeThrough(Y, X):
							new_start = r_slope
							continue
						else:
							blocked = False
							start = new_start
					else:
						if not level.seeThrough(Y, X) and j < radius:
							# This is a blocking square, start a child scan:
							blocked = True
							self._cast_light(level, cy, cx, j+1, start, l_slope, radius, xx, xy, yx, yy)
							new_start = r_slope
			# Row is scanned; do next row unless last square was blocked:
			if blocked:
				break

