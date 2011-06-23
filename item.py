from dice import Dice

types = set()
types.add = "weapon"
types.add = "shield"
types.add = "armor"
types.add = "hat"
types.add = "boots"


class Item:
	def __init__(self, _type=(), equippable=(), stats=()):
		self.type = _type
		self.equippable = equippable
		self.stats = stats


#class Weapon(Item):
#	def __init__(self, dice=None, equippable=("left_hand", "right_hand"), stats=()):
#		if dice:
#			dice = Dice()
#		self.damage_dice = dice
#		super().__init__(("weapon", ), stats)
