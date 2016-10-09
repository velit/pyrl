from creature.advanced_creature import AdvancedCreature
from creature.equipment import Slot
from creature.item import Weapon, Armor
from creature.stats import Stat
from creature.template import CreatureTemplate
from enums.colors import Color, Pair
from dice import Dice


def Player():
    template = CreatureTemplate("tappi", ('@', (Color.Green, Color.Black)), observe_level_change=True)
    player = AdvancedCreature(template)

    armor_stats = (
        (Stat.accuracy, 10),
        (Stat.speed, 100),
    )
    armor = Armor("Armor of Kings", 10, 10, [Slot.Body], armor_stats, (']', Pair.Yellow))
    player.equipment.equip(armor, Slot.Body)

    # weapon = Weapon("Black Spike", 15, Dice(8, 8, 10), two_handed=True, char=('(', Pair.Darkest))
    # player.equipment.equip(weapon, Slot.Right_Hand)

    weapon = Weapon("Sting", 0, Dice(1, 8, 20), char=('(', Pair.Green))
    player.equipment.equip(weapon, Slot.Right_Hand)

    armor = Armor("Protector", 12, 20, [Slot.Right_Hand, Slot.Left_Hand], [(Stat.endurance, 2)])
    player.equipment.equip(armor, Slot.Left_Hand)

    items = (
        Weapon("Short Sword",       0, Dice(1, 6, 1)),
        Weapon("Long Sword",        0, Dice(1, 8, 0)),
        Weapon("Short Sword",       0, Dice(1, 6, 1)),
        Weapon("Short Sword",       0, Dice(1, 6, 2)),
        Weapon("Long Sword",        0, Dice(1, 8, 1)),
        Weapon("Short Sword",       0, Dice(1, 6, -1)),
        Weapon("Short Sword",       0, Dice(1, 6, 3)),
        Weapon("Short Sword",       0, Dice(1, 6, 0)),
        Weapon("Long Sword",        0, Dice(1, 8, 2)),
        Weapon("Lance of Longinus", 0, Dice(4, 8, 8), stats=[(Stat.endurance, 8)], char=('(', Pair.Red)),
    )
    items = items + tuple(Weapon("Short Sword", i, (1, 6, i)) for i in range(60))
    for itam in items:
        player.equipment.bag_item(itam)

    return player
