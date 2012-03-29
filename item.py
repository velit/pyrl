from dice import Dice

#types = {
	#"weapon",
	#"shield",
	#"armor",
	#"hat",
	#"boots",
#}


class Item(object):
	def __init__(self, name, stats={}):
		self.name = name
		self.stats = stats

	def __str__(self):
		if self.stats:
			stats = ", ".join("{0[0]}:{0[1]}".format(x) for x in self.stats.viewitems())
			stats = "{" + stats + "}"
		else:
			stats = ""
		return "{0.name} {1}".format(self, stats)


class Weapon(Item):
	def __init__(self, name, dice=1, sides=6, addition=0, stats={}):
		self.damage = Dice(dice, sides, addition)
		Item.__init__(self, name, stats)

	def roll(self):
		return self.damage.roll()

	def __str__(self):
		stats = ", ".join("{0[0]}: {0[1]}".format(x) for x in self.stats.viewitems())
		return "{0.name} ({0.damage}) {1}".format(self, stats)
