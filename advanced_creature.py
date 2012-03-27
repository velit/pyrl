from creature import Creature
from const.slots import HEAD, BODY, FEET, HANDS
from const.stats import *

class AdvancedCreature(Creature):

	def __init__(self, creature_file):
		super(self.__class__, self).__init__(creature_file)

		self.slots = {}
		self.slots[HANDS] = None
		self.slots[HEAD] = None
		self.slots[BODY] = None
		self.slots[FEET] = None
		self.inventory = []

		self.last_action_energy = 0


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

	def get_item(self, slot):
		return self.slots[slot]

	def get_item_stats(self, STAT):
		return sum(item.stats[STAT] for item in self.slots.viewvalues() if item is not None and STAT in item.stats)

	def update_energy(self, amount):
		super(self.__class__, self).update_energy(amount)
		self.last_action_energy = amount

	def update_energy_action(self, action):
		self.last_action_energy = super(self.__class__, self).update_energy_action(action)

	def is_idle(self):
		return False

	def equip(self, item, slot):
		self.slots[slot] = item

	def unequip(self, slot):
		item = self.slots[slot]
		self.slots[slot] = None
		return item

	def bag_item(self, item):
		self.inventory.append(item)

	def unbag_item(self, item):
		self.inventory.remove(item)

	def get_inventory_lines(self):
		f = "{1}. {0.name} {0.stats}"
		for i, item in enumerate(self.inventory):
			yield f.format(item, (i + 1) % 10)

	@property
	def sight(self):
		return super(self.__class__, self).sight + self.get_item_stats(SIGHT)

	@property
	def max_hp(self):
		return super(self.__class__, self).max_hp + self.get_item_stats(MAX_HP)

	@property
	def dmg_bonus(self):
		return super(self.__class__, self).dmg_bonus + self.get_item_stats(DMG_BONUS)

	@property
	def pv(self):
		return super(self.__class__, self).pv + self.get_item_stats(PV)

	@property
	def ar(self):
		return super(self.__class__, self).ar + self.get_item_stats(AR)

	@property
	def dr(self):
		return super(self.__class__, self).dr + self.get_item_stats(DR)

	@property
	def unarmed_dice(self):
		return super(self.__class__, self).unarmed_dice + self.get_item_stats(UNARMED_DICE)

	@property
	def unarmed_sides(self):
		return super(self.__class__, self).unarmed_sides + self.get_item_stats(UNARMED_SIDES)

	@property
	def speed(self):
		return super(self.__class__, self).speed + self.get_item_stats(SPEED)
