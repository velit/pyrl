from __future__ import annotations

from collections import Counter

from pyrl.engine.creature.enums.slots import Slot
from pyrl.engine.world.item import Weapon, Armor
from pyrl.engine.creature.advanced.player import Player
from pyrl.engine.creature.advanced.skills import Skills, Skill
from pyrl.engine.creature.enums.stats import Stat
from pyrl.engine.structures.dice import Dice
from pyrl.engine.enums.glyphs import Colors

def pyrl_player() -> Player:
    skills = Skills(Counter({
        Skill.HEALING: 20
    }))
    player = Player(skills, "player")
    aok = Armor("Armor of Kings", 1000, 1000, [Slot.Body], {Stat.ACC: 10, Stat.SPEED: 100}, (']', Colors.Yellow))
    player.inventory.equip(aok, Slot.Body)

    # weapon = Weapon("Black Spike", 15, Dice(8, 8, 10), two_handed=True, glyph=('(', ColorPairs.Darkest))
    # player.equipment.equip(weapon, Slot.Right_Hand)

    sting = Weapon("Sting", 0, Dice(1, 8, 20), glyph=('(', Colors.Green))
    player.inventory.equip(sting, Slot.Right_Hand)

    aok = Armor("Protector", 12, 20, [Slot.Right_Hand, Slot.Left_Hand], {Stat.END: 2})
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
        Weapon("Lance of Longinus", 100, Dice(4, 8, 8), stats={Stat.END: 8}, glyph=('(', Colors.Red)),
    )
    items2 = tuple(Weapon("Short Sword", i, Dice(1, 6, i)) for i in range(60))
    for item in (items + items2):
        player.inventory.bag_item(item)
    return player
