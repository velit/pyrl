from __future__ import annotations

import code
import sys
from collections.abc import Callable

from pyrl.config.binds import Binds
from pyrl.config.debug import Debug
from pyrl.engine.actions.action_exceptions import NoValidTargetException
from pyrl.engine.actions.action_feedback import ActionFeedback, NoActionFeedback
from pyrl.engine.actions.action_interface import ActionInterface
from pyrl.engine.structures.helper_mixins import CreatureActionsMixin
from pyrl.engine.world.enums.level_location import LevelLocation
from pyrl.game_data.levels.shared_assets import DefaultLocation

class DebugAction(CreatureActionsMixin):

    def __init__(self, actions: ActionInterface) -> None:
        self.actions = actions

        self.action_funcs: dict[str, Callable[[], ActionFeedback | None]] = {
            'a': self.add_monster,
            'c': self.display_curses_color_info,
            'd': self.show_path_debug,
            'g': self.print_user_input,
            'i': self.interactive_console,
            'k': self.kill_creatures_in_level,
            'm': self.print_message_debug_string,
            'o': self.draw_path_to_passage_down,
            'p': self.draw_path_from_up_to_down,
            'r': self.toggle_path_heuristic_cross,
            'v': self.show_map,
            'x': self.descend_to_end,
            'y': self.toggle_log_keycodes,
            'X': self.ascend_to_surface,
        }

    def ask_action(self) -> ActionFeedback:
        c = self.io.get_key("Avail cmds: " + "".join(sorted(self.action_funcs.keys())))
        if c in self.action_funcs:
            feedback = self.action_funcs[c]()
            return feedback if feedback is not None else NoActionFeedback
        self.io.msg(f"Undefined debug key: {c}")
        return NoActionFeedback

    def print_user_input(self) -> None:
        self.io.msg(self.io.get_str("Tulostetaas tää: "))

    def add_monster(self) -> ActionFeedback | None:
        if self.level.ongoing_creature_spawns:
            self.level.spawn_creature(self.level.creature_picker.spawn_random_creature())
            return self.actions.debug_action()
        else:
            self.io.msg("No ongoing spawning on this level. Can't add monster.")
            return None

    def show_map(self) -> ActionFeedback:
        Debug.show_map = not Debug.show_map
        self.io.msg(f"Show map set to {Debug.show_map}")
        return self.actions.redraw_action()

    def toggle_path_heuristic_cross(self) -> None:
        Debug.cross = not Debug.cross
        self.io.msg(f"Path heuristic cross set to {Debug.cross}")

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

    def kill_creatures_in_level(self) -> ActionFeedback:
        creature_list = list(self.level.creatures.values())
        creature_list.remove(self.creature)
        for i in creature_list:
            self.level.remove_creature(i)
        self.io.msg("Abracadabra.")
        return self.actions.debug_action()

    def draw_path_to_passage_down(self) -> ActionFeedback:
        passage_down_coord = self.level.get_location_coord(DefaultLocation.Passage_Down)
        self.io.draw_path(self.level.path(self.creature.coord, passage_down_coord))
        return self.actions.redraw_action()

    def draw_path_from_up_to_down(self) -> ActionFeedback:
        passage_up_coord = self.level.get_location_coord(DefaultLocation.Passage_Up)
        passage_down_coord = self.level.get_location_coord(DefaultLocation.Passage_Down)
        self.io.draw_path(self.level.path(passage_up_coord, passage_down_coord))
        return self.actions.redraw_action()

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
        if sys.platform != "win32":
            import curses
            self.io.msg(f"{curses.COLORS=} {curses.COLOR_PAIRS=} {curses.can_change_color()=}")
        else:
            self.io.msg("Not running curses")

    def print_message_debug_string(self) -> None:
        self.io.msg(Debug.debug_string)

    def sight_change(self, amount: int) -> ActionFeedback:
        raise NotImplementedError

    def teleport_to_location(self, location: LevelLocation) -> ActionFeedback:
        try:
            new_coord = self.level.get_location_coord(location)
        except KeyError:
            raise NoValidTargetException(f"This level doesn't seem to have a {location} location")
        if not self.level.is_passable(new_coord):
            self.level.remove_creature(self.level.creatures[new_coord])
        return self.actions.teleport(new_coord)

    def descend_to_end(self) -> None:
        from tests.integration_tests import dummy_plug_system
        dummy_plug_system.get().add_input([Binds.Descend.key] * 200)

    def ascend_to_surface(self) -> None:
        from tests.integration_tests import dummy_plug_system
        dummy_plug_system.get().add_input([Binds.Ascend.key] * 200)
