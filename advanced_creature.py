from creature import Creature
from const.slots import HEAD, BODY, FEET, HANDS
from const.stats import *

class AdvancedCreature(Creature):

	def __init__(self, creature_file):
		self.slots = {}
		self.slots[HANDS] = None
		self.slots[HEAD] = None
		self.slots[BODY] = None
		self.slots[FEET] = None

		self.last_action_energy = 0

		super().__init__(creature_file)

	def get_damage_info(self):
		if self.slots[HANDS] is not None:
			dice = self.slots[HANDS].dice
			sides = self.slots[HANDS].sides
			addition = self.slots[HANDS].addition + self.dmg_bonus
		else:
			dice = self.unarmed_dice
			sides = self.unarmed_sides
			addition = self.dmg_bonus
		return dice, sides, addition

	def equip(self, item, slot):
		self.slots[slot] = item

	def unequip(self, slot):
		self.slots[slot] = None

	def get_item_stats(self, STAT):
		return sum(item.stats[STAT] for item in self.slots.values() if item is not None and STAT in item.stats)

	def update_energy(self, amount):
		super().update_energy(amount)
		self.last_action_energy = amount

	def update_energy_action(self, action):
		self.last_action_energy = super().update_energy_action(action)

	@property
	def sight(self):
		return super().sight + self.get_item_stats(SIGHT)

	@property
	def max_hp(self):
		return super().max_hp + self.get_item_stats(MAX_HP)

	@property
	def dmg_bonus(self):
		return super().dmg_bonus + self.get_item_stats(DMG_BONUS)

	@property
	def pv(self):
		return super().pv + self.get_item_stats(PV)

	@property
	def ar(self):
		return super().ar + self.get_item_stats(AR)

	@property
	def dr(self):
		return super().dr + self.get_item_stats(DR)

	@property
	def unarmed_dice(self):
		return super().unarmed_dice + self.get_item_stats(UNARMED_DICE)

	@property
	def unarmed_sides(self):
		return super().unarmed_sides + self.get_item_stats(UNARMED_SIDES)

	@property
	def speed(self):
		return super().speed ++ self.get_item_stats(SPEED)
