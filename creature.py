import curses
from random import randrange, randint, choice
from pio import io
from char import Char

# Multipliers for transforming coordinates to other octants:
mult = [[1, 0, 0, -1, -1, 0, 0, 1],
		[0, 1, -1, 0, 0, -1, 1, 0],
		[0, 1, 1, 0, 0, -1, -1, 0],
		[1, 0, 0, 1, -1, 0, 0, -1]]


class Creature:
	"""This is an abstract class representing a creature"""

	def __init__(self, game, level):
		self.name = "creature"
		self.n = "him"
		self.ch = Char('@', "white")
		self.g = game
		self.l = level
		self.visibility = set()
		self.visi_mod = set()
		self.hostile = False
		self.reverse = ""

	def attack(self, creature):
		attack_succeeds, damage = self._attack(creature)
		if attack_succeeds:
			if creature is self.g.p:
				if damage > 0:
					msg = "The {} hits you for {} damage."
					io.msg(msg.format(self.name, damage))
				else:
					msg = "The {} fails to hurt you."
					io.msg(msg.format(self.name))
			else:
				if damage > 0:
					msg = "The {} hits the {} for {} damage."
					io.msg(msg.format(self.name, creature.name, damage))
				else:
					msg = "The {} fails to hurt {}."
					io.msg(msg.format(self.name, creature.name))
			creature.lose_hp(damage)
		elif creature is self.g.p:
			msg = "The {} misses you."
			io.msg(msg.format(self.name))
		else:
			msg = "The {} misses the {}."
			io.msg(msg.format(self.name, creature.name))

	def _attack(self, creature):
		roll = randint(1,100) + self.ar - creature.ar
		if roll > 25:
			return (True, max(self.dmg - creature.pv, 0))
		else:
			return (False, 0)

	def getloc(self):
		return self.l.getsquare(creature=self).getloc()

	def getsquare(self):
		return self.l.getsquare(creature=self)

	def act(self):
		self.move_random()

	def act_towards(self, y, x, c=(-1, 1)):
		# Self
		sy, sx = self.getloc()

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

		#TODO: make more aesthethically pleasing at some point
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

	def exit_level(self):
		self.l.enter_passage(self.getsquare().getexit())

	def rcs(self, y, x, hostile=True):
		"""Right click square (rts games)"""
		if self.l.legal_loc(y, x):
			s = self.l.getsquare(y, x)
			if s.passable():
				self.l.movecreature(self, s)
			elif s.creature is self.g.p:
				self.attack(s.creature)
			else:
				return True
		return False

	def move(self, y, x):
		if self.l.legal_loc(y, x):
			targetsquare = self.l.getsquare(y, x)
			if targetsquare.passable():
				self.l.movecreature(self, targetsquare)
			elif targetsquare.creature is not None:
				self.attack(targetsquare.creature)
			return True
		return False

	def move_random(self):
		sy, sx = self.getloc()
		for i in range(5):
			r = randrange(9) + 1
			y = sy - 1 + r // 3
			x = sx - 1 + r % 3
			if self.rcs(y, x):
				return True
		return False

	def lose_hp(self, amount):
		self.hp -= amount
		if self.hp <= 0:
			self.die()

	def die(self):
		io.msg("The " + self.name + " dies.")
		self.l.removecreature(self)

	def has_range(self, square):
		sy, sx = self.getloc()
		return (sy - square.y) ** 2 + (sx - square.x) ** 2 <= self.sight ** 2

	def has_los(self, square):
		return self.has_range(square) and \
				self.l.check_los(self.getsquare(), square)

	def redraw_view(self):
		self.visibility.clear()
		self.l.drawmemory()
		self.update_view()

	def update_view(self):
		#self.update_los()
		self.l.drawmap()

	def update_los(self):
		old = self.visibility
		self.visibility = set()
		self.cast_light()
		io.clearlos(old - self.visibility, self.l)
		io.drawlos(self.visibility - (old - self.visi_mod), self.l, self.reverse)
		self.visi_mod.clear()

	def cast_light(self):
		y, x = self.getloc()
		if self.sight > 0:
			self.l.visit_square(y, x)
		for oct in range(8):
			self._cast_light(self.l, y, x, 1, 1.0, 0.0, self.sight,
					mult[0][oct], mult[1][oct], mult[2][oct], mult[3][oct])

	# Algorithm by Bjorn Bergstrom bjorn.bergstrom@roguelikedevelopment.org
	# Copyright 2001
	# http://roguebasin.roguelikedevelopment.org/
	# index.php?title=FOV_using_recursive_shadowcasting

	def _cast_light(self, level, cy, cx, row, start, end, r, xx, xy, yx, yy):
		"""Recursive lightcasting function"""
		if start < end:
			return
		radius_squared = r * r
		for j in range(row, r + 1):
			dx, dy = 0 - 1 - j, 0 - j
			blocked = False
			while dx <= 0:
				dx += 1
				# Translate the dx, dy coordinates into map coordinates:
				X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
				# l_slope and r_slope store the slopes of the left and right
				# extremities of the square we're considering:
				l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
				if start < r_slope:
					continue
				elif end > l_slope:
					break
				else:
					# Our light beam is touching this square; light it:
					if dx * dx + dy * dy <= radius_squared:
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
							self._cast_light(level, cy, cx, j + 1, start,
												l_slope, r, xx, xy, yx, yy)
							new_start = r_slope
			# Row is scanned; do next row unless last square was blocked:
			if blocked:
				break
