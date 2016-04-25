from __future__ import absolute_import, division, print_function, unicode_literals

from enums.colors import Color
from creature.equipment import Slot
from creature.stats import Stat
from creature.advanced_creature import AdvancedCreature
from creature.item import Item, Weapon
from creature.template import CreatureTemplate
from enums.colors import Pair


def Player():
    template = CreatureTemplate("tappi", ('@', (Color.Green, Color.Black)), observe_level_change=True)
    player = AdvancedCreature(template)

    armor_stats = (
        (Stat.armor, 4),
        (Stat.attack_rating, 100),
        (Stat.defense_rating, 170),
        (Stat.speed, 100),
        (Stat.sight, 0),
    )
    armor_slots = (Slot.Body, )
    armor = Item("Armor of Kings", armor_slots, (']', Pair.Yellow), armor_stats)
    player.equipment.equip(armor, Slot.Body)

    weapon = Weapon("Sting", (1, 8, 20), char=('(', Pair.Green))
    player.equipment.equip(weapon, Slot.Right_Hand)

    items = (
        Weapon("short sword +1",    (1, 6, 1)),
        Weapon("long sword",        (1, 8, 0)),
        Weapon("short sword +1",    (1, 6, 1)),
        Weapon("short sword +2",    (1, 6, 2)),
        Weapon("long sword +1",     (1, 8, 1)),
        Weapon("short sword -1",    (1, 6, -1)),
        Weapon("short sword +3",    (1, 6, 3)),
        Weapon("short sword",       (1, 6, 0)),
        Weapon("long sword +2",     (1, 8, 2)),
        Weapon("Lance of longinus", (4, 8, 8), char=('(', Pair.Red)).add_stat(Stat.endurance,  8),
    )
    items = items + tuple(Weapon("short sword +" + str(i), (1, 6, i)) for i in range(60))
    for itam in items:
        player.equipment.bag_item(itam)

    return player
