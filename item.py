from dice import dice_roll

#types = set()
#types.add = "weapon"
#types.add = "shield"
#types.add = "armor"
#types.add = "hat"
#types.add = "boots"


class Item:
	def __init__(self, stats=()):
		#self.type = _type
		#self.equippable = equippable
		self.stats = stats


class Weapon(Item):
	def __init__(self, dice=1, sides=6, addition=0, stats=()):
		self.dice = dice
		self.sides = sides
		self.addition = addition
		super().__init__(stats)

	def roll(self):
		return dice_roll(self.dice, self.sides, self.addition)
