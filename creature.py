import curses
from random import randrange as rr
from random import choice
from io import io

# Multipliers for transforming coordinates to other octants:
mult = [[1,  0,  0, -1, -1,  0,  0,  1],
		[0,  1, -1,  0,  0, -1,  1,  0],
		[0,  1,  1,  0,  0, -1, -1,  0],
		[1,  0,  0,  1, -1,  0,  0, -1]]

class Creature(object):
	"""This is an abstract class representing a creature"""
	def __init__(self, game, level):
		self.sight = 15
		self.hp = 10
		self.dmg = 1
		self.g = game
		self.l = level
		self.square = None
		self.visibility = set()
		self.visi_mod = set()
		self.hostile = False
		self.reverse = ""

	def getloc(self):
		return self.square.y, self.square.x

	def act(self):
		self.move_random()

	def act_towards(self, y, x, c=(-1,1)):
		# Self
		sy = self.square.y
		sx = self.square.x

		# Difference
		dy = y - sy
		dx = x - sx

		# Modifier
		my, mx = 0, 0
		
		if dy > 0:
			my = 1
		elif dy < 0:
			my = -1
		if dx > 0:
			mx = 1
		elif dx < 0:
			mx = -1

		if self.rcs(sy + my, sx + mx):
			r = choice(c)
			if my == 0:
				if self.rcs(sy + r, sx + mx):
					if self.rcs(sy - r, sx + mx):
						if self.rcs(sy + r, sx):
							if self.rcs(sy - r, sx):
								if self.rcs(sy + r, sx - mx):
									if self.rcs(sy - r, sx - mx):
										self.rcs(sy, sx - mx)
			elif mx == 0:
				if self.rcs(sy + my, sx + r):
					if self.rcs(sy + my, sx - r):
						if self.rcs(sy, sx + r):
							if self.rcs(sy, sx - r):
								if self.rcs(sy - my, sx + r):
									if self.rcs(sy - my, sx - r):
										self.rcs(sy - my, sx - mx)
			elif abs(dy) > abs(dx):
				if self.rcs(sy + my, sx):
					if self.rcs(sy, sx + mx):
						if self.rcs(sy + my, sx - mx):
							if self.rcs(sy - my, sx + mx):
								if self.rcs(sy, sx - mx):
									if self.rcs(sy - my, sx):
										self.rcs(sy - my, sx - mx)
			elif abs(dy < abs(dx)):
				if self.rcs(sy, sx + mx):
					if self.rcs(sy + my, sx):
						if self.rcs(sy - my, sx + mx):
							if self.rcs(sy + my, sx - mx):
								if self.rcs(sy - my, sx):
									if self.rcs(sy, sx - mx):
										self.rcs(sy - my, sx - mx)
			elif r == 1:
				if self.rcs(sy + my, sx):
					if self.rcs(sy, sx + mx):
						if self.rcs(sy + my, sx - mx):
							if self.rcs(sy - my, sx + mx):
								if self.rcs(sy, sx - mx):
									if self.rcs(sy - my, sx):
										self.rcs(sy - my, sx - mx)
			elif r == -1:
				if self.rcs(sy, sx + mx):
					if self.rcs(sy + my, sx):
						if self.rcs(sy - my, sx + mx):
							if self.rcs(sy + my, sx - mx):
								if self.rcs(sy - my, sx):
									if self.rcs(sy, sx - mx):
										self.rcs(sy - my, sx - mx)

	# Right click square (rts games)
	def rcs(self, y, x, hostile=True):
		if self.l.legal_yx(y, x):
			s = self.l.getsquare(y, x)
			if s.passable():
				self.l.movecreature(self, s)
			elif s.creature is self.g.p:
				self.hit(s.creature)
			else:
				return True
		return False

	def move_random(self):
		for i in range(5):
			y = self.square.y + rr(3) - 1
			x = self.square.x + rr(3) - 1
			if self.l.legal_yx(y, x):
				self.rcs(self.square.y + rr(3) - 1, self.square.x + rr(3) - 1)
				return

	def lose_hp(self, amount):
		self.hp -= amount
		if self.hp <= 0:
			self.die()

	def die(self):
		io.msg("The "+self.name+" dies.")
		self.l.removecreature(self)

	def hit(self, creature):
		if creature is self.g.p:
			io.msg("The "+self.name+" hits the you.")
		else:
			io.msg("The "+self.name+" hits the "+creature.name+".")
		creature.lose_hp(self.dmg)

	def has_range(self, square):
		sy, sx = self.getloc()
		py, px = square.y, square.x
		return (sy-py)*(sy-py) + (sx-px)*(sx-px) <= self.sight*self.sight

	def has_los(self, square):
		return self.has_range(square) and \
				self.l.check_los(self.square, square)

	def update_los(self):
		old = self.visibility
		self.visibility = set()
		self.cast_light()
		io.clearlos(old - self.visibility, self.l)
		io.drawlos(self.visibility -(old -self.visi_mod), self.l, self.reverse)
		self.visi_mod.clear()

	def cast_light(self):
		y, x = self.square.y, self.square.x
		if self.sight > 0:
			self.l.visit_square(y,x)
		for oct in range(8):
			self._cast_light(self.l, y, x, 1, 1.0, 0.0, self.sight,
					mult[0][oct], mult[1][oct], mult[2][oct], mult[3][oct])

	# Algorithm by Bjorn Bergstrom bjorn.bergstrom@roguelikedevelopment.org
	# Copyright 2001 
	# http://roguebasin.roguelikedevelopment.org/ \
	# index.php?title=FOV_using_recursive_shadowcasting
	def _cast_light(self, level, cy, cx, row, start, end, r, xx, xy, yx, yy):
		"Recursive lightcasting function"
		if start < end:
			return
		radius_squared = r*r
		for j in range(row, r+1):
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
					if dx*dx + dy*dy <= radius_squared:
						self.l.visit_square(Y, X)
					if blocked:
						# we're scanning a row of blocked squares:
						if not level.see_through(Y, X):
							new_start = r_slope
							continue
						else:
							blocked = False
							start = new_start
					else:
						if not level.see_through(Y, X) and j < r:
							# This is a blocking square, start a child scan:
							blocked = True
							self._cast_light(level, cy, cx, j+1, start,
												l_slope, r, xx, xy, yx, yy)
							new_start = r_slope
			# Row is scanned; do next row unless last square was blocked:
			if blocked:
				break

