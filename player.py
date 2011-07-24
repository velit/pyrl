from creature import Creature
from monster_file import MonsterFile
from char import Char
from item import Item, Weapon
from const.stats import *
from const.slots import *


def Player():
	monster_file = MonsterFile("tappi", Char('@', "blue"), 0, 0)
	player = Creature(monster_file)

	armor_stats = ((PV, 5), (DR, 10))
	player.stat.equip(Item(armor_stats), BODY)

	weapon = Weapon(1, 8, 2)
	player.stat.equip(weapon, HANDS)

	return player
