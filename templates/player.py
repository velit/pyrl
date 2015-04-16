from __future__ import absolute_import, division, print_function, unicode_literals

from const.colors import Color
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
    player.equip(armor, Slot.body)

    weapon = Weapon("Sting", 1, 8, 20)
    player.equip(weapon, Slot.right_hand)

    itams = (
        Weapon("+1 short sword", 1, 6, 1),
        Weapon("+0 long sword", 1, 8, 0),
        Weapon("+1 short sword", 1, 6, 1),
        Weapon("+2 short sword", 1, 6, 2),
        Weapon("+1 long sword", 1, 8, 1),
        Weapon("-1 short sword", 1, 6, -1),
        Weapon("+3 short sword", 1, 6, 3),
        Weapon("+0 short sword", 1, 6, 0),
        Weapon("Lance of longinus", 4, 8, 8).add_stat(Stat.endurance, 8),
        Weapon("+2 long sword", 1, 8, 2),
    )
    for itam in itams:
        player.bag_item(itam)

    return player
