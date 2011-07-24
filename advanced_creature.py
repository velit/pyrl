from creature import Creature
from const.slots import HEAD, BODY, FEET, HANDS

class AdvancedCreature(Creature):

	def __init__(self, creature_file):
		super().__init__(creature_file)

		self.slots = {}
		self.slots[HANDS] = None
		self.slots[HEAD] = None
		self.slots[BODY] = None
		self.slots[FEET] = None
		self.inventory = []

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
