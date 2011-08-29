from advanced_creature import AdvancedCreature
from monster_file import MonsterFile
from char import Char
from item import Item, Weapon
from const.stats import *
from const.slots import *


def Player():
	monster_file = MonsterFile("tappi", Char('@', "blue"), 0, 0)
	player = AdvancedCreature(monster_file)

	armor_stats = {PV: 0, DR: 10}
	player.equip(Item(armor_stats), BODY)

	weapon = Weapon(1, 8, 2)
	player.equip(weapon, HANDS)

	return player
