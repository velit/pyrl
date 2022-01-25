from __future__ import annotations

from typing import TYPE_CHECKING

from pyrl.creature.creature import Creature
from pyrl.creature.mixins.learner import Learner
from pyrl.creature.stats import Stat

if TYPE_CHECKING:
    from pyrl.window.window_system import WindowSystem
    from pyrl.game import Game

def register_status_texts(io: WindowSystem, game: Game, creature: Creature) -> None:
    io.status_bar.elements.clear()
    register = io.status_bar.add_element
    register("Lvl", lambda: creature.experience_level if isinstance(creature, Learner) else creature.creature_level)
    register("Dmg",                   lambda: creature.damage_dice)
    register("HP",                    lambda: f"{creature.hp}/{creature.max_hp}")
    register(Stat.accuracy.value,     lambda: creature.accuracy)
    register(Stat.defense.value,      lambda: creature.defense)
    register(Stat.armor.value,        lambda: creature.armor)
    register(Stat.sight.value,        lambda: creature.sight)
    register(Stat.speed.value,        lambda: creature.speed)
    register(Stat.regen.value,        lambda: creature.regen)
    register("Loc",                   lambda: f"{creature.level.level_key.dungeon}/{creature.level.level_key.idx:02}")
    register(Stat.strength.value,     lambda: creature.strength)
    register(Stat.dexterity.value,    lambda: creature.dexterity)
    register(Stat.intelligence.value, lambda: creature.intelligence)
    register(Stat.endurance.value,    lambda: creature.endurance)
    register(Stat.perception.value,   lambda: creature.perception)
    # register("Loc",                   lambda: ",".join(f"{dim:02}" for dim in creature.coord))
    register("Turns",                 lambda: creature.turns)
    register("Time",                  lambda: f"{creature.time / 1000:.2f}s")
