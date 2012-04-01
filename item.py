import const.slots as SLOT
from dice import Dice

def get_stats_str(stats):
	stats_str = ", ".join("{0}:{1}".format(stat, value) for stat, value in stats.viewitems())
	return "{" + stats_str + "}"


class Item(object):
	def __init__(self, name):
		self.name = name
		self.stats = {}
		self.compatible_slots = set()

	def __str__(self):
		if self.stats:
			stats_str = get_stats_str(self.stats)
			return "{0.name} {1}".format(self, stats_str)
		else:
			return "{0.name}".format(self)

	def add_stat(self, stat, value):
		self.stats[stat] = value
		return self

	def add_slot(self, slot):
		self.compatible_slots.add(slot)
		return self

	def get_stat_bonus(self, stat):
		if stat in self.stats:
			return self.stats[stat]
		else:
			return 0

	def fits_to_slot(self, slot):
		return slot in self.compatible_slots


class Weapon(Item):
	def __init__(self, name, dice=1, sides=6, addition=0):
		super(Weapon, self).__init__(name)
		self.damage = Dice(dice, sides, addition)
		self.add_slot(SLOT.RIGHT_HAND)

	def roll(self):
		return self.damage.roll()

	def get_damage(self):
		return self.damage.get_values()

	def __str__(self):
		if self.stats:
			stats_str = get_stats_str(self.stats)
			return "{0.name} ({0.damage}) {1}".format(self, stats_str)
		else:
			return "{0.name} ({0.damage})".format(self)
