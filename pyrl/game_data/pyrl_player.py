from __future__ import annotations

from pyrl.creature.item import Armor, Weapon
from pyrl.creature.player import Player
from pyrl.creature.stats import Stats
from pyrl.structures.dice import Dice
from pyrl.types.color import Color, Colors
from pyrl.types.equipment_slot import Slot

def pyrl_player() -> Player:
    player = Player("player", ('@', (Color.Green, Color.Black)))
    aok = Armor("Armor of Kings", 1000, 1000, [Slot.Body], Stats(accuracy=10, speed=100), (']', Colors.Yellow))
    player.inventory.equip(aok, Slot.Body)

    # weapon = Weapon("Black Spike", 15, Dice(8, 8, 10), two_handed=True, char=('(', ColorPairs.Darkest))
    # player.equipment.equip(weapon, Slot.Right_Hand)

    sting = Weapon("Sting", 0, Dice(1, 8, 20), char=('(', Colors.Green))
    player.inventory.equip(sting, Slot.Right_Hand)

    aok = Armor("Protector", 12, 20, [Slot.Right_Hand, Slot.Left_Hand], Stats(endurance=2))
    player.inventory.equip(aok, Slot.Left_Hand)

    items = (
        Weapon("Short Sword", 0, Dice(1, 6, 1)),
        Weapon("Long Sword", 0, Dice(1, 8, 0)),
        Weapon("Short Sword", 0, Dice(1, 6, 1)),
        Weapon("Short Sword", 0, Dice(1, 6, 2)),
        Weapon("Long Sword", 0, Dice(1, 8, 1)),
        Weapon("Short Sword", 0, Dice(1, 6, -1)),
        Weapon("Short Sword", 0, Dice(1, 6, 3)),
        Weapon("Short Sword", 0, Dice(1, 6, 0)),
        Weapon("Long Sword", 0, Dice(1, 8, 2)),
        Weapon("Lance of Longinus", 100, Dice(4, 8, 8), stats=Stats(endurance=8), char=('(', Colors.Red)),
    )
    items2 = tuple(Weapon("Short Sword", i, Dice(1, 6, i)) for i in range(60))
    for itam in (items + items2):
        player.inventory.bag_item(itam)
    return player
