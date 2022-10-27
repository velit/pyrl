from __future__ import annotations

from typing import TYPE_CHECKING

from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.mixins.learner import Learner
from pyrl.engine.creature.stats import Stat

if TYPE_CHECKING:
    from pyrl.ui.window.window_system import WindowSystem
    from pyrl.engine.game import Game

def register_status_texts(io: WindowSystem, game: Game, creature: Creature) -> None:
    io.status_bar.elements.clear()
    register = io.status_bar.add_element
    register("Lvl", lambda: creature.experience_level if isinstance(creature, Learner) else creature.creature_level)
    register("Dmg",                   lambda: creature.damage_dice)
    register("HP",                    lambda: f"{creature.hp}/{creature.max_hp}")
    register(Stat.accuracy,           lambda: creature.accuracy)
    register(Stat.defense,            lambda: creature.defense)
    register(Stat.armor,              lambda: creature.armor)
    register(Stat.sight,              lambda: creature.sight)
    register(Stat.speed,              lambda: creature.speed)
    register(Stat.regen,              lambda: creature.regen)
    register("Loc",                   lambda: f"{creature.level.level_key.dungeon}/{creature.level.level_key.idx:02}")
    register(Stat.strength,           lambda: creature.strength)
    register(Stat.dexterity,          lambda: creature.dexterity)
    register(Stat.intelligence,       lambda: creature.intelligence)
    register(Stat.endurance,          lambda: creature.endurance)
    register(Stat.perception,         lambda: creature.perception)
    # register("Loc",                   lambda: ",".join(f"{dim:02}" for dim in creature.coord))
    register("Turns",                 lambda: creature.turns)
    register("Time",                  lambda: f"{creature.time / 1000:.2f}s")
