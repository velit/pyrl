from __future__ import annotations

from typing import TYPE_CHECKING

from pyrl.creature.creature import Creature
from pyrl.creature.stats import Stat

if TYPE_CHECKING:
    from pyrl.window.window_system import WindowSystem
    from pyrl.game import Game

def register_status_texts(io: WindowSystem, game: Game, creature: Creature) -> None:
    register = io.status_bar.add_element
    register("Dmg",                   lambda: creature.damage_dice)
    register("HP",                    lambda: f"{creature.hp}/{creature.max_hp}")
    register(Stat.sight.value,        lambda: creature.sight)
    register(Stat.accuracy.value,     lambda: creature.accuracy)
    register(Stat.defense.value,      lambda: creature.defense)
    register(Stat.armor.value,        lambda: creature.armor)
    register(Stat.speed.value,        lambda: creature.speed)
    register("Loc",                   lambda: ",".join(f"{dim:02}" for dim in creature.coord))
    register("Wloc",                  lambda: f"{creature.level.level_key.dungeon}/{creature.level.level_key.idx:02}")
    register(Stat.strength.value,     lambda: creature.strength)
    register(Stat.dexterity.value,    lambda: creature.dexterity)
    register(Stat.intelligence.value, lambda: creature.intelligence)
    register(Stat.endurance.value,    lambda: creature.endurance)
    register(Stat.perception.value,   lambda: creature.perception)
    register("Turns",                 lambda: game.turn_counter)
    register("Game Time",             lambda: game.time)
    register("Level Time",            lambda: creature.level.turn_scheduler.time)
