from __future__ import absolute_import, division, print_function, unicode_literals
from creature.stats import Stat


def register_status_texts(game, creature):
    add_element = game.io.status_bar.add_element
    add_element("Dmg",                      lambda: "{}D{}+{}".format(*creature.get_damage_info()))
    add_element("HP",                       lambda: "{}/{}".format(creature.hp, creature.max_hp))
    add_element(Stat.sight.value,           lambda: creature.sight)
    add_element(Stat.attack_rating.value,   lambda: creature.attack_rating)
    add_element(Stat.defense_rating.value,  lambda: creature.defense_rating)
    add_element(Stat.armor.value,           lambda: creature.armor)
    add_element(Stat.speed.value,           lambda: creature.speed)
    add_element(Stat.strength.value,        lambda: creature.strength)
    add_element(Stat.dexterity.value,       lambda: creature.dexterity)
    add_element(Stat.intelligence.value,    lambda: creature.intelligence)
    add_element(Stat.endurance.value,       lambda: creature.endurance)
    add_element(Stat.perception.value,      lambda: creature.perception)
    add_element("Wloc",                     lambda: "{}/{}".format(*creature.level.world_loc))
    add_element("Loc",                      lambda: "{0:02},{1:02}".format(*creature.coord))
    add_element("Turns",                    lambda: game.turn_counter)
    add_element("Game Time",                lambda: game.time)
    add_element("Level Time",               lambda: creature.level.turn_scheduler.time)
