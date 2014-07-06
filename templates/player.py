from __future__ import absolute_import, division, print_function, unicode_literals

import const.colors as COLOR
import const.slots as SL
import const.stats as ST
from advanced_creature import AdvancedCreature
from item import Item, Weapon
from monster_template import MonsterTemplate


def Player():
    monster_template = MonsterTemplate("tappi", ('@', (COLOR.BASE_BLACK, COLOR.BASE_GREEN)), 0, 0)
    player = AdvancedCreature(monster_template)

    armor = Item("Armor of Kings")
    armor.add_stat(ST.PV, 4)
    armor.add_stat(ST.AR, 100)
    armor.add_stat(ST.DR, 170)
    armor.add_stat(ST.SPEED, 100)
    armor.add_stat(ST.SIGHT, 0)
    armor.add_slot(SL.BODY)
    player.equip(armor, SL.BODY)

    weapon = Weapon("Sting", 1, 8, 20)
    player.equip(weapon, SL.RIGHT_HAND)

    itams = (
        Weapon("+1 short sword", 1, 6, 1),
        Weapon("+0 long sword", 1, 8, 0),
        Weapon("+1 short sword", 1, 6, 1),
        Weapon("+2 short sword", 1, 6, 2),
        Weapon("+1 long sword", 1, 8, 1),
        Weapon("-1 short sword", 1, 6, -1),
        Weapon("+3 short sword", 1, 6, 3),
        Weapon("+0 short sword", 1, 6, 0),
        Weapon("Lance of longinus", 4, 8, 8).add_stat(ST.TO, 8),
        Weapon("+2 long sword", 1, 8, 2),
    )
    for itam in itams:
        player.bag_item(itam)

    return player
