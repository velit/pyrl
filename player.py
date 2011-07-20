import curses

from creature import Creature
from char import Char
from pio import io
from item import Item, Weapon
from const.game import DEFAULT
from const.stats import *
from const.slots import *


class Player(Creature):
	"""da player object"""

	def __init__(self, game):
		super().__init__(game)
		self.name = "tappi"
		self.n = "god"
		self.char = Char('@', "blue")

		armor_stats = ((PV, 5), (DR, 10))
		self.stat.equip(Item(armor_stats), BODY)

		weapon = Weapon(1, 8, 2)
		self.stat.equip(weapon, HANDS)

		self.register_status_texts()

	def register_status_texts(self):
		io.s.add_element("dmg", "DMG: ", lambda: "{}D{}+{}".format(
				*self.stat.get_damage_info()))
		io.s.add_element("hp", "HP: ", lambda: "{}/{}".format(self.hp, self.stat.max_hp))
		io.s.add_element("sight", "sight: ", lambda: self.stat.sight)
		io.s.add_element("turns", "TC: ", lambda: self.g.turn_counter)
		io.s.add_element("loc", "Loc: ", lambda:self.l.world_loc)
		io.s.add_element("ar", "AR: ", lambda: self.stat.ar)
		io.s.add_element("dr", "DR: ", lambda: self.stat.dr)
		io.s.add_element("pv", "PV: ", lambda: self.stat.pv)

	#def attack(self, creature):
	#	attack_succeeds, damage = self._attack(creature)
	#	if attack_succeeds:
	#		if damage > 0:
	#			io.msg("You hit the {} for {} damage.".format(creature.name, damage))
	#			creature.lose_hp(damage)
	#		else:
	#			io.msg("You fail to hurt the {}.".format(creature.name))
	#	else:
	#		io.msg("You miss the {}.".format(creature.name))

	def die(self):
		io.sel_getch("You die... [more]", char_list=DEFAULT)
		self.g.endgame(False)
