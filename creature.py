import curses
from random import randrange, randint, choice
from pio import io
from char import Char
from creature_stats import Stats
from fov import get_light_set


class Creature:
	"""This is an abstract class representing a creature"""

	def __init__(self, game):
		self.name = "creature"
		self.n = "him"
		self.char = Char('@', "white")
		self.g = game
		self.turn_visibility = set()
		self.turn_mod = set()
		self.level_memory = {}
		self.hostile = False
		self.reverse = ""
		self.stat = Stats()
		self.hp = self.stat.max_hp
		self.level_loc = None

	@property
	def l(self):
		return self.g.cur_level

	def lose_hp(self, amount):
		self.hp -= amount
		if self.hp <= 0:
			self.die()

	def die(self):
		io.msg("The " + self.name + " dies.")
		self.l.removecreature(self)

	def drawmemory(self):
		io.clearlos(self.level_memory[self.l.world_loc], self.l)

	def redraw_view(self):
		io.clear_level()
		self.turn_visibility.clear()
		self.turn_mod.clear()
		self.drawmemory()
		self.update_view()

	def update_view(self):
		self.update_los()
		#self.l.draw()

	def get_coord(self):
		return self.l.get_coord(self.loc)

	def update_los(self):
		old = self.turn_visibility
		new = get_light_set(self.l.see_through, self.get_coord(), self.stat.sight, self.l.cols)
		mod = self.turn_mod

		io.clearlos(old - new, self.l)
		io.drawlos(new - (old - mod), self.l, self.reverse)
		self.level_memory[self.l.world_loc] |= new
		self.turn_visibility = new
		self.turn_mod.clear()

	#def attack(self, creature):
	#	attack_succeeds, damage = self._attack(creature)
	#	if attack_succeeds:
	#		if creature is self.g.player:
	#			if damage > 0:
	#				msg = "The {} hits you for {} damage."
	#				io.msg(msg.format(self.name, damage))
	#			else:
	#				msg = "The {} fails to hurt you."
	#				io.msg(msg.format(self.name))
	#		else:
	#			if damage > 0:
	#				msg = "The {} hits the {} for {} damage."
	#				io.msg(msg.format(self.name, creature.name, damage))
	#			else:
	#				msg = "The {} fails to hurt {}."
	#				io.msg(msg.format(self.name, creature.name))
	#		creature.lose_hp(damage)
	#	elif creature is self.g.player:
	#		msg = "The {} misses you."
	#		io.msg(msg.format(self.name))
	#	else:
	#		msg = "The {} misses the {}."
	#		io.msg(msg.format(self.name, creature.name))

	#def _attack(self, creature):
	#	roll = randint(1, 100) + self.stat.ar - creature.stat.ar
	#	if roll > 25:
	#		return (True, max(self.stat.damage_roll() - creature.stat.pv, 0))
	#	else:
	#		return (False, 0)

	#def act(self):
	#	self.move_random()

	#def act_towards(self, y, x, c=(-1, 1)):
	#	# Self
	#	sy, sx = self.getcoord()

	#	# Difference
	#	dy = y - sy
	#	dx = x - sx

	#	# Modifier
	#	my, mx = 0, 0

	#	if dy > 0:
	#		my = 1
	#	elif dy < 0:
	#		my = -1
	#	if dx > 0:
	#		mx = 1
	#	elif dx < 0:
	#		mx = -1

	#	#TODO: make more aesthethically pleasing at some point
	#	if self.rcs(sy + my, sx + mx):
	#		r = choice(c)
	#		if my == 0:
	#			if self.rcs(sy + r, sx + mx):
	#				if self.rcs(sy - r, sx + mx):
	#					if self.rcs(sy + r, sx):
	#						if self.rcs(sy - r, sx):
	#							if self.rcs(sy + r, sx - mx):
	#								if self.rcs(sy - r, sx - mx):
	#									self.rcs(sy, sx - mx)
	#		elif mx == 0:
	#			if self.rcs(sy + my, sx + r):
	#				if self.rcs(sy + my, sx - r):
	#					if self.rcs(sy, sx + r):
	#						if self.rcs(sy, sx - r):
	#							if self.rcs(sy - my, sx + r):
	#								if self.rcs(sy - my, sx - r):
	#									self.rcs(sy - my, sx - mx)
	#		elif abs(dy) > abs(dx):
	#			if self.rcs(sy + my, sx):
	#				if self.rcs(sy, sx + mx):
	#					if self.rcs(sy + my, sx - mx):
	#						if self.rcs(sy - my, sx + mx):
	#							if self.rcs(sy, sx - mx):
	#								if self.rcs(sy - my, sx):
	#									self.rcs(sy - my, sx - mx)
	#		elif abs(dy < abs(dx)):
	#			if self.rcs(sy, sx + mx):
	#				if self.rcs(sy + my, sx):
	#					if self.rcs(sy - my, sx + mx):
	#						if self.rcs(sy + my, sx - mx):
	#							if self.rcs(sy - my, sx):
	#								if self.rcs(sy, sx - mx):
	#									self.rcs(sy - my, sx - mx)
	#		elif r == 1:
	#			if self.rcs(sy + my, sx):
	#				if self.rcs(sy, sx + mx):
	#					if self.rcs(sy + my, sx - mx):
	#						if self.rcs(sy - my, sx + mx):
	#							if self.rcs(sy, sx - mx):
	#								if self.rcs(sy - my, sx):
	#									self.rcs(sy - my, sx - mx)
	#		elif r == -1:
	#			if self.rcs(sy, sx + mx):
	#				if self.rcs(sy + my, sx):
	#					if self.rcs(sy - my, sx + mx):
	#						if self.rcs(sy + my, sx - mx):
	#							if self.rcs(sy - my, sx):
	#								if self.rcs(sy, sx - mx):
	#									self.rcs(sy - my, sx - mx)

	#def rcs(self, y, x, hostile=True):
	#	"""Right click square (rts games)"""
	#	if self.l.legal_coord(y, x):
	#		s = self.l.getsquare(y, x)
	#		if s.passable():
	#			self.l.movecreature(self, s)
	#		elif s.creature is self.g.player:
	#			self.attack(s.creature)
	#		else:
	#			return True
	#	return False

	#def move(self, y, x):
	#	if self.l.legal_coord(y, x):
	#		targetsquare = self.l.getsquare(y, x)
	#		if targetsquare.passable():
	#			self.l.movecreature(self, targetsquare)
	#		elif targetsquare.creature is not None:
	#			self.attack(targetsquare.creature)
	#		return True
	#	return False

	#def move_random(self):
	#	sy, sx = self.getcoord()
	#	for i in range(5):
	#		r = randrange(9) + 1
	#		y = sy - 1 + r // 3
	#		x = sx - 1 + r % 3
	#		if self.rcs(y, x):
	#			return True
	#	return False

	#def has_range(self, loc):
	#	sy, sx = self.getcoord()
	#	ty, tx = self.l.getcoord(loc)

	#	return (sy - ty) ** 2 + (sx - tx) ** 2 <= self.stat.sight ** 2

	#def has_los(self, loc):
	#	return self.has_range(loc) and self.l.check_los(self.getsquare(), square)
