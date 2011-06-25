from const.slots import *
from dice import dice_roll


class Base_Stats:
	def __init__(self, parent_object):
		self._dict = {}
		self._parent_object = parent_object
		self._enabled = False

	def __getitem__(self, key):
		return self._dict[key]

	def __setitem__(self, key, value):
		self._dict[key] = value
		if self._enabled:
			self._parent_object.update_stats()

	def __delitem__(self, key):
		del self._dict[key]
		if self._enabled:
			self._parent_object.update_stats()

	def enable(self):
		self.enabled = True

class Stats:
	def __init__(self):
		self.str = None
		self.dex = None
		self.con = None
		self.int = None
		self.per = None

		self.sight = None
		self.max_hp = None
		self.dmg_bonus = None
		self.pv = None
		self.ar = None
		self.dr = None
		self.unarmed_dice = None
		self.unarmed_sides = None
		self.unarmed_dmg_bonus = None

		self.slots = {}
		self.slots[HANDS] = None
		self.slots[HEAD] = None
		self.slots[BODY] = None
		self.slots[FEET] = None
		self.inventory = []

		self.base = Base_Stats(self)
		self.base["str"] = 10
		self.base["dex"] = 10
		self.base["con"] = 10
		self.base["int"] = 10
		self.base["per"] = 10
		self.base.enable()

		self.update_stats()

	def update_stats(self):
		self.str = self.base["str"]
		self.dex = self.base["dex"]
		self.con = self.base["con"]
		self.int = self.base["int"]
		self.per = self.base["per"]

		self.sight = 6 + (self.per - 10) // 2
		self.dmg_bonus = self.str // 5
		self.armed_dmg_bonus = 0
		self.unarmed_dmg_bonus = 0
		self.unarmed_dice = self.str // 20 + 1
		self.unarmed_sides = self.str // 3 + self.dex // 6
		self.pv = self.con // 10
		self.ar = self.dex + self.int // 2
		self.dr = self.dex + self.int // 2
		self.max_hp = self.con + self.str // 2

		for item in self.slots.values():
			if item is not None:
				for stat, value in item.stats:
					setattr(self, stat, getattr(self, stat) + value)

	def equip(self, item, slot):
		self.slots[slot] = item
		self.update_stats()

	def unequip(self, slot):
		self.slots[slot] = None
		self.update_stats()

	def get_damage_info(self):
		if self.slots[HANDS] is not None:
			dice = self.slots[HANDS].dice
			sides = self.slots[HANDS].sides
			addition = self.slots[HANDS].addition + self.armed_dmg_bonus + self.dmg_bonus
		else:
			dice = self.unarmed_dice
			sides = self.unarmed_sides
			addition = self.unarmed_dmg_bonus + self.dmg_bonus
		return dice, sides, addition

	def damage_roll(self):
		return dice_roll(*self.get_damage_info())

#BASE_STATS = ("base_str", "base_dex", "base_con", "base_int")

#def add_base_stat_properties(cls, stat):
#	real_attribute = "_" + stat
#	def g(self):
#		return getattr(self, real_attribute)
#	def s(self, value):
#		setattr(self, real_attribute, value)
#		self.update_stats()
#	def d(self):
#		delattr(self, real_attribute)
#	setattr(cls, stat, property(g, s, d))


#for stat in BASE_STATS:
#	add_base_stat_properties(Stats, stat)
