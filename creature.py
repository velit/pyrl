from char import Char
from const.slots import *


class Creature:

	def __init__(self, creature_file):
		self.name = creature_file.name
		self.char = creature_file.char
		self.loc = None

		self.str = 10
		self.dex = 10
		self.con = 10
		self.int = 10
		self.per = 10

		self.hp = self.max_hp

	def equip(self, item, slot):
		self.slots[slot] = item

	def unequip(self, slot):
		self.slots[slot] = None

	def get_damage_info(self):
		dice = self.unarmed_dice
		sides = self.unarmed_sides
		addition = self.dmg_bonus
		return dice, sides, addition

	@property
	def sight(self):
		return 6 + (self.per - 10) // 2

	@property
	def max_hp(self):
		return self.con + self.str // 2

	@property
	def dmg_bonus(self):
		return self.str // 5

	@property
	def pv(self):
		return self.con // 10

	@property
	def ar(self):
		return self.dex + self.int // 2

	@property
	def dr(self):
		return self.dex + self.int // 2

	@property
	def unarmed_dice(self):
		return self.str // 20 + 1

	@property
	def unarmed_sides(self):
		return self.str // 3 + self.dex // 6
