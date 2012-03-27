from dice import dice_roll

#types = {
	#"weapon",
	#"shield",
	#"armor",
	#"hat",
	#"boots",
#}


class Item(object):
	def __init__(self, name, stats=()):
		self.name = name
		self.stats = stats


class Weapon(Item):
	def __init__(self, name, dice=1, sides=6, addition=0, stats=()):
		self.dice = dice
		self.sides = sides
		self.addition = addition
		Item.__init__(self, name, stats)

	def roll(self):
		return dice_roll(self.dice, self.sides, self.addition)
