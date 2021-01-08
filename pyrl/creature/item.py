from pyrl.enums.slot import Slot
from pyrl.enums.colors import Pair
from pyrl.creature.stats import Stat, ComplexStat
from pyrl.dice import dice_str

def Weapon(name, accuracy, weapon_dice, two_handed=False, compatible_slots=(Slot.Right_Hand, Slot.Left_Hand),
           stats=(), char=('(', Pair.Normal)):
    stats = ((ComplexStat.weapon_dice, weapon_dice), (Stat.accuracy, accuracy), *stats)
    return Item(name=name, compatible_slots=compatible_slots, stats=stats, char=char,
                occupies_all_slots=two_handed)

def Armor(name, defense, armor_value, compatible_slots=(), stats=(), char=(']', Pair.Normal)):
    stats = ((Stat.defense, defense), (Stat.armor, armor_value), *stats)
    return Item(name=name, compatible_slots=compatible_slots, stats=stats, char=char,
                occupies_all_slots=False)

class Item:
    def __init__(self, name, compatible_slots, stats, char, occupies_all_slots):
        self.name = name
        self.compatible_slots = tuple(compatible_slots)
        self.stats = tuple(stats)
        self.char = char
        self.occupies_all_slots = occupies_all_slots

    def fits_slot(self, slot):
        return slot in self.compatible_slots

    def get_stat(self, stat, default=None):
        for stat0, value in self.stats:
            if stat0 is stat:
                return value
        return default

    def weapon_str(self):
        weapon_dice = self.get_stat(ComplexStat.weapon_dice)
        accuracy = self.get_stat(Stat.accuracy, default=0)
        if weapon_dice is not None:
            return " ({:+}, {})".format(accuracy, dice_str(*weapon_dice))
        elif accuracy:
            return " ({:+})".format(accuracy)
        else:
            return ""

    def armor_str(self):
        defense = self.get_stat(Stat.defense, default=0)
        armor_value = self.get_stat(Stat.armor, default=0)
        if defense or armor_value:
            return " [{:+}, {:+}]".format(defense, armor_value)
        else:
            return ""

    def stats_str(self):
        skip_stats = (Stat.accuracy, ComplexStat.weapon_dice, Stat.defense, Stat.armor)
        stats = ", ".join("{}:{:+}".format(stat.value, value) for stat, value in self.stats if stat not
                          in skip_stats)
        if stats:
            return " {%s}" % stats
        else:
            return ""

    def __str__(self):
        return "{}{}{}{}".format(self.name, self.weapon_str(), self.armor_str(), self.stats_str())

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return ("Item(name={self.name}, "
                "char={self.char}, "
                "compatible_slots={self.compatible_slots}, "
                "stats={self.stats})").format(self=self)
