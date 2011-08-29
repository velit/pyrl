from char import Char
from const.slots import *


class Creature:

	def __init__(self, creature_file):
		self.name = creature_file.name
		self.char = creature_file.char
		self.loc = None
		self.target_loc = None
		self.target_dir = None

		self.strength = 10
		self.dexterity = 10
		self.toughness = 10
		self.intelligence = 10
		self.perception = 10

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

	def lose_hp(self, amount):
		if amount > 0:
			self.hp -= amount
		return self.hp <= 0

	@property
	def sight(self):
		return 6 + (self.perception - 10) // 2

	@property
	def max_hp(self):
		return self.toughness + self.strength // 2

	@property
	def dmg_bonus(self):
		return self.strength // 5

	@property
	def pv(self):
		return self.toughness // 10

	@property
	def ar(self):
		return self.dexterity + self.intelligence // 2

	@property
	def dr(self):
		return self.dexterity + self.intelligence // 2

	@property
	def unarmed_dice(self):
		return self.strength // 20 + 1

	@property
	def unarmed_sides(self):
		return self.strength // 3 + self.dexterity // 6
