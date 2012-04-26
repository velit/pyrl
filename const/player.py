import const.colors as COLOR
from advanced_creature import AdvancedCreature
from monster_file import MonsterFile
from item import Item, Weapon
from const.stats import *
from const.slots import *


def Player():
    monster_file = MonsterFile("tappi", ('@', (COLOR.BASE_BLACK, COLOR.BASE_GREEN)), 0, 0)
    player = AdvancedCreature(monster_file)

    armor = Item("Armor of Kings")
    armor.add_stat(PV, 4)
    armor.add_stat(AR, 100)
    armor.add_stat(DR, 170)
    armor.add_stat(SPEED, 100)
    armor.add_stat(SIGHT, 0)
    armor.add_slot(BODY)
    player.equip(armor, BODY)

    weapon = Weapon("Sting", 1, 8, 20)
    player.equip(weapon, RIGHT_HAND)

    itams = (
        Weapon("+1 short sword", 1, 6, 1),
        Weapon("+0 long sword", 1, 8, 0),
        Weapon("+1 short sword", 1, 6, 1),
        Weapon("+2 short sword", 1, 6, 2),
        Weapon("+1 long sword", 1, 8, 1),
        Weapon("-1 short sword", 1, 6, -1),
        Weapon("+3 short sword", 1, 6, 3),
        Weapon("+0 short sword", 1, 6, 0),
        Weapon("Lance of longinus", 4, 8, 8).add_stat(TO, 8),
        Weapon("+2 long sword", 1, 8, 2),
    )
    for itam in itams:
        player.bag_item(itam)

    return player
