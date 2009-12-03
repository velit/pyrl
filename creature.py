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
	def __init__(self, level):
		self.sight = 8
		self.hp = 50
		self.l = level
		self.visibility = []

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

	def visitSquare(self, y, x):
		self.l.visitSquare(y,x)
		self.visibility.append((y,x))

	def updateLos(self):
		io.clearLos(self.visibility, self.l)
		y,x = self.l.squares[self].y, self.l.squares[self].x
		if self.sight != 0:
			self.visitSquare(y,x)
		for oct in range(8):
			self._cast_light(self.l, y, x, 1, 1.0, 0.0, self.sight, mult[0][oct], mult[1][oct], mult[2][oct], mult[3][oct])
		io.drawLos(self.visibility, self.l)
