from __future__ import annotations

from typing import TYPE_CHECKING

from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.mixins.turner import Turner
from pyrl.engine.creature.stats import Stat

if TYPE_CHECKING:
    from pyrl.ui.window.window_system import WindowSystem
    from pyrl.engine.game import Game


def register_status_texts(io: WindowSystem, game: Game, creature: Creature) -> None:
    io.status_bar.elements.clear()
    register = io.status_bar.add_element
    register("Lvl",                 lambda: creature.creature_level)
    register("Dmg",                 lambda: creature.damage_dice)
    register("HP",                  lambda: f"{creature.hp}/{creature[Stat.MAX_HP]}")
    register(Stat.ACC.short_name,   lambda: creature[Stat.ACC])
    register(Stat.DEF.short_name,   lambda: creature[Stat.DEF])
    register(Stat.ARMOR.short_name, lambda: creature[Stat.ARMOR])
    register(Stat.SIGHT.short_name, lambda: creature[Stat.SIGHT])
    register(Stat.SPEED.short_name, lambda: creature[Stat.SPEED])
    register(Stat.REGEN.short_name, lambda: creature[Stat.REGEN])
    register("Loc",                 lambda: f"{creature.level.level_key.dungeon}/{creature.level.level_key.idx:02}")
    register(Stat.STR.short_name,   lambda: creature[Stat.STR])
    register(Stat.DEX.short_name,   lambda: creature[Stat.DEX])
    register(Stat.INT.short_name,   lambda: creature[Stat.INT])
    register(Stat.END.short_name,   lambda: creature[Stat.END])
    register(Stat.PER.short_name,   lambda: creature[Stat.PER])
    register("Turns",               lambda: creature.turns if isinstance(creature, Turner) else 0)
    register("Time", lambda: f"{creature.ticks / 1000:.2f}s")
