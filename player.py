import const.colors as COLOR
from advanced_creature import AdvancedCreature
from monster_file import MonsterFile
from char import Char
from item import Item, Weapon
from const.stats import *
from const.slots import *


def Player():
	monster_file = MonsterFile("tappi", Char('@', (COLOR.BASE_BLACK, COLOR.BASE_GREEN)), 0, 0)
	player = AdvancedCreature(monster_file)

	armor_stats = {PV: 4, AR:100, DR: 170, SPEED: 100}
	player.equip(Item(armor_stats), BODY)

	weapon = Weapon(1, 8, 20)
	player.equip(weapon, HANDS)

	return player
