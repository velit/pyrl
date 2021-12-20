from pyrl.creature.creature import Creature
from pyrl.creature.item import Weapon, Armor
from pyrl.creature.mixins.has_inventory import HasInventory
from pyrl.creature.mixins.remembers_vision import RemembersVision
from pyrl.creature.stats import Stats
from pyrl.dice import Dice
from pyrl.enums.colors import Color, ColorPair
from pyrl.enums.equipment_slot import Slot

class Player(HasInventory, RemembersVision, Creature):
    def __init__(self) -> None:
        super().__init__(name="player", char=('@', (Color.Green, Color.Black)))

        aok = Armor("Armor of Kings", 10, 10, [Slot.Body], Stats(accuracy=10, speed=100), (']', ColorPair.Yellow))
        self.inventory.equip(aok, Slot.Body)

        # weapon = Weapon("Black Spike", 15, Dice(8, 8, 10), two_handed=True, char=('(', ColorPair.Darkest))
        # self.equipment.equip(weapon, Slot.Right_Hand)

        sting = Weapon("Sting", 0, Dice(1, 8, 20), char=('(', ColorPair.Green))
        self.inventory.equip(sting, Slot.Right_Hand)

        aok = Armor("Protector", 12, 20, [Slot.Right_Hand, Slot.Left_Hand], Stats(endurance=2))
        self.inventory.equip(aok, Slot.Left_Hand)

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
            Weapon("Lance of Longinus", 0, Dice(4, 8, 8), stats=Stats(endurance=8), char=('(', ColorPair.Red)),
        )
        items2 = tuple(Weapon("Short Sword", i, Dice(1, 6, i)) for i in range(60))
        for itam in (items + items2):
            self.inventory.bag_item(itam)
