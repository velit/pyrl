from __future__ import absolute_import, division, print_function, unicode_literals

from enums.colors import Color
from creature.equipment import Slot
from creature.stats import Stat
from creature.advanced_creature import AdvancedCreature
from creature.item import Item, Weapon
from monster_template import MonsterTemplate


def Player():
    monster_template = MonsterTemplate("tappi", ('@', (Color.Green, Color.Black)), 0, 0)
    player = AdvancedCreature(monster_template)

    armor_stats = (
        (Stat.armor, 4),
        (Stat.attack_rating, 100),
        (Stat.defense_rating, 170),
        (Stat.speed, 100),
        (Stat.sight, 0),
    )
    armor_slots = (Slot.body, )
    armor = Item("Armor of Kings", armor_stats, armor_slots)
    player.equipment.bag_item(armor)
    player.equipment.equip(armor, Slot.body)

    weapon = Weapon("Sting", 1, 8, 20)
    player.equipment.bag_item(weapon)
    player.equipment.equip(weapon, Slot.right_hand)

    itams = (
        Weapon("short sword +1",     1,  6,  1),
        Weapon("long sword",         1,  8,  0),
        Weapon("short sword +1",     1,  6,  1),
        Weapon("short sword +2",     1,  6,  2),
        Weapon("long sword +1",      1,  8,  1),
        Weapon("short sword -1",     1,  6,  -1),
        Weapon("short sword +3",     1,  6,  3),
        Weapon("short sword",        1,  6,  0),
        Weapon("long sword +2",      1,  8,  2),
        Weapon("Lance of longinus",  4,  8,  8).add_stat(Stat.endurance,  8),
    )
    itams = itams + tuple(Weapon("short sword +" + str(i), 1, 6, i) for i in range(60))
    for itam in itams:
        player.equipment.bag_item(itam)

    return player
