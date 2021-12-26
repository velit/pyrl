from __future__ import annotations

import code
from collections.abc import Callable
from typing import Literal

from pyrl.config.binds import Binds
from pyrl.config.debug import Debug
from pyrl.types.level_gen import LevelGen
from pyrl.types.level_location import LevelLocation
from pyrl.creature.actions import Action, NoValidTargetException
from pyrl.game_actions import GameActions
from pyrl.structures.helper_mixins import GameActionsMixin
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.world.level import Level

class DebugAction(GameActionsMixin):

    def __init__(self, game_actions: GameActions) -> None:
        self.actions = game_actions

        self.action_funcs: dict[str, Callable[[], Action | None]] = {
            'a': self.add_monster,
            'c': self.display_curses_color_info,
            'd': self.show_path_debug,
            'g': self.print_user_input,
            'i': self.interactive_console,
            'k': self.kill_creatures_in_level,
            'l': self.cycle_level_type,
            'm': self.print_message_debug_string,
            'o': self.draw_path_to_passage_down,
            'p': self.draw_path_from_up_to_down,
            'r': self.toggle_path_heuristic_cross,
            'v': self.show_map,
            'x': self.descend_to_end,
            'y': self.toggle_log_keycodes,
            'X': self.ascend_to_surface,
        }

    def ask_action(self) -> Action:
        c = self.io.get_key("Avail cmds: " + "".join(sorted(self.action_funcs.keys())))
        if c in self.action_funcs:
            action = self.action_funcs[c]()
            return action if action is not None else Action.Debug
        self.io.msg(f"Undefined debug key: {c}")
        return Action.No_Action

    def print_user_input(self) -> None:
        self.io.msg(self.io.get_str("Tulostetaas tää: "))

    def add_monster(self) -> None:
        if self.level.creature_spawning_enabled:
            self.level.spawn_creature(self.level.creature_spawner.random_creature())
            self.actions.no_action()
        else:
            self.io.msg("No random spawning on this level. Can't add monster.")

    def show_map(self) -> None:
        Debug.show_map = not Debug.show_map
        self.actions.redraw()
        self.io.msg(f"Show map set to {Debug.show_map}")

    def toggle_path_heuristic_cross(self) -> None:
        Debug.cross = not Debug.cross
        self.io.msg(f"Path heuristic cross set to {Debug.cross}")

    def cycle_level_type(self) -> None:
        last_level_type: LevelGen | str = "All levels are already generated"
        level: Level
        for level in self.world.levels.values():
            if level.is_finalized:
                continue
            if level.generation_type == LevelGen.Dungeon:
                level.generation_type = LevelGen.Arena
            elif level.generation_type == LevelGen.Arena:
                level.generation_type = LevelGen.Dungeon
            last_level_type = level.generation_type
        self.io.msg(f"Level type set to {last_level_type}")

    def show_path_debug(self) -> None:
        if not Debug.path:
            Debug.path = True
            self.io.msg("Path debug set")
        elif not Debug.path_step:
            Debug.path_step = True
            self.io.msg("Path debug and stepping set")
        else:
            Debug.path = False
            Debug.path_step = False
            self.io.msg("Path debug unset")

    def kill_creatures_in_level(self) -> None:
        creature_list = list(self.level.creatures.values())
        creature_list.remove(self.creature)
        for i in creature_list:
            self.level.remove_creature(i)
        self.actions.no_action()
        self.io.msg("Abracadabra.")

    def draw_path_to_passage_down(self) -> None:
        passage_down_coord = self.level.get_location_coord(DefaultLocation.Passage_Down)
        self.io.draw_path(self.level.path(self.creature.coord, passage_down_coord))
        self.actions.redraw()

    def draw_path_from_up_to_down(self) -> None:
        passage_up_coord = self.level.get_location_coord(DefaultLocation.Passage_Up)
        passage_down_coord = self.level.get_location_coord(DefaultLocation.Passage_Down)
        self.io.draw_path(self.level.path(passage_up_coord, passage_down_coord))
        self.actions.redraw()

    def interactive_console(self) -> None:
        self.io.suspend()
        game = self.actions.game
        io = self.io
        player = self.creature
        level = self.level
        code.interact(local=locals())
        self.io.resume()

    def toggle_log_keycodes(self) -> None:
        Debug.show_keycodes = not Debug.show_keycodes
        self.io.msg(f"Input code debug set to {Debug.show_keycodes}")

    def display_curses_color_info(self) -> None:
        import curses
        self.io.msg(f"{curses.COLORS=} {curses.COLOR_PAIRS=} {curses.can_change_color()=}")

    def print_message_debug_string(self) -> None:
        self.io.msg(Debug.debug_string)

    def sight_change(self, amount: int) -> Action:
        self.creature.base_perception += amount
        return self.actions.no_action()

    def teleport_to_location(self, location: LevelLocation) -> Literal[Action.Teleport]:
        try:
            new_coord = self.level.get_location_coord(location)
        except KeyError:
            raise NoValidTargetException(f"This level doesn't seem to have a {location} location")
        if not self.level.is_passable(new_coord):
            self.level.remove_creature(self.level.creatures[new_coord])
        return self.actions.teleport(new_coord)

    def descend_to_end(self) -> None:
        self.io.prepared_input.extend([Binds.Descend.key] * 200)

    def ascend_to_surface(self) -> None:
        self.io.prepared_input.extend([Binds.Ascend.key] * 200)
