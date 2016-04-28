from creature.equipment import Slot
from dice import Dice
from enums.colors import Pair


def get_stats_str(stats):
    stats_str = ", ".join("{0}:{1}".format(stat.value, value) for stat, value in stats)
    return "{" + stats_str + "}"


class Item(object):
    def __init__(self, name, compatible_slots=(), char=(']', Pair.Normal), stats=()):
        self.name = name
        self.char = char
        self.compatible_slots = tuple(compatible_slots)
        self.stats = tuple(stats)

    def __str__(self):
        if self.stats:
            stats_str = get_stats_str(self.stats)
            return "{0.name} {1}".format(self, stats_str)
        else:
            return "{0.name}".format(self)

    def add_stat(self, stat, value):
        self.stats += ((stat, value), )
        return self

    def add_stats(self, stats):
        self.stats += stats
        return self

    def fits_to_slot(self, slot):
        return slot in self.compatible_slots

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return "Item(name={name}, char={char}, compatible_slots={compatible_slots}, stats={stats})".format(**self.__dict__)


class Weapon(Item):
    def __init__(self, name, dice_stats, compatible_slots=(Slot.Right_Hand, Slot.Left_Hand),
                 char=('(', Pair.Normal), stats=()):
        super().__init__(name, compatible_slots, char, stats)
        dice, sides, addition = dice_stats
        self.damage = Dice(dice, sides, addition)

    def roll(self):
        return self.damage.roll()

    def get_damage(self):
        return self.damage.get_values()

    def __str__(self):
        if self.stats:
            stats_str = get_stats_str(self.stats)
            return "{0.name} ({0.damage}) {1}".format(self, stats_str)
        else:
            return "{0.name} ({0.damage})".format(self)
