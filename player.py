import curses

from creature import Creature
from char import Char
from item import Item, Weapon
from const.stats import *
from const.slots import *


def Player():
	player = Creature()
	player.name = "tappi"
	player.n = "god"
	player.char = Char('@', "blue")

	armor_stats = ((PV, 5), (DR, 10))
	player.stat.equip(Item(armor_stats), BODY)

	weapon = Weapon(1, 8, 2)
	player.stat.equip(weapon, HANDS)

	return player

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

	#def die(self):
	#	io.sel_getch("You die... [more]", char_list=DEFAULT)
	#	self.g.endgame(False)
