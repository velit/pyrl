from __future__ import annotations

from typing import TYPE_CHECKING

from pyrl.creature.player import Player
from pyrl.creature.stats import Stat

if TYPE_CHECKING:
    from pyrl.window.window_system import WindowSystem
    from pyrl.game import Game

def register_status_texts(io: WindowSystem, game: Game, player: Player) -> None:
    register = io.status_bar.add_element
    register("Lvl",                   lambda: player.experience_level)
    register("Dmg",                   lambda: player.damage_dice)
    register("HP",                    lambda: f"{player.hp}/{player.max_hp}")
    register(Stat.accuracy.value,     lambda: player.accuracy)
    register(Stat.defense.value,      lambda: player.defense)
    register(Stat.armor.value,        lambda: player.armor)
    register(Stat.sight.value,        lambda: player.sight)
    register(Stat.speed.value,        lambda: player.speed)
    register("Turns",                 lambda: game.turn_counter)
    register("Loc",                   lambda: f"{player.level.level_key.dungeon}/{player.level.level_key.idx:02}")
    register(Stat.strength.value,     lambda: player.strength)
    register(Stat.dexterity.value,    lambda: player.dexterity)
    register(Stat.intelligence.value, lambda: player.intelligence)
    register(Stat.endurance.value,    lambda: player.endurance)
    register(Stat.perception.value,   lambda: player.perception)
    # register("Loc",                   lambda: ",".join(f"{dim:02}" for dim in player.coord))
    # register("Game Time",             lambda: game.time)
    # register("Level Time",            lambda: creature.level.turn_scheduler.time)
