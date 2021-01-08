from pyrl.enums.slot import Slot
from pyrl.creature.item import Weapon, Armor
from pyrl.creature.stats import Stat
from pyrl.enums.colors import Color, Pair
from pyrl.dice import Dice
from pyrl.creature.creature import Creature
from pyrl.creature.has_equipment import HasEquipment
from pyrl.creature.remembers_vision import RemembersVision

class Player(HasEquipment, RemembersVision, Creature):
    def __init__(self):
        super().__init__(name="player", char=('@', (Color.Green, Color.Black)))

        armor_stats = (
            (Stat.accuracy, 10),
            (Stat.speed, 100),
        )
        armor = Armor("Armor of Kings", 10, 10, [Slot.Body], armor_stats, (']', Pair.Yellow))
        self.equipment.equip(armor, Slot.Body)

        # weapon = Weapon("Black Spike", 15, Dice(8, 8, 10), two_handed=True, char=('(', Pair.Darkest))
        # self.equipment.equip(weapon, Slot.Right_Hand)

        weapon = Weapon("Sting", 0, Dice(1, 8, 20), char=('(', Pair.Green))
        self.equipment.equip(weapon, Slot.Right_Hand)

        armor = Armor("Protector", 12, 20, [Slot.Right_Hand, Slot.Left_Hand], [(Stat.endurance, 2)])
        self.equipment.equip(armor, Slot.Left_Hand)

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
            self.equipment.bag_item(itam)
