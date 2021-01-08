import code

from pyrl.binds import Binds
from pyrl.config.debug import Debug
from pyrl.game_actions import GameActionsProperties, feedback, Action
from pyrl.enums.level_gen import LevelGen
from pyrl.enums.level_location import LevelLocation

class DebugAction(GameActionsProperties, object):

    def __init__(self, game_actions):
        self.actions = game_actions

        self.action_funcs = {
            'a': self.add_monster,
            'c': self.display_curses_color_info,
            'd': self.show_path_debug,
            'i': self.interactive_console,
            'k': self.kill_creatures_in_level,
            'l': self.cycle_level_type,
            'm': self.print_message_debug_string,
            'g': self.print_user_input,
            'o': self.draw_path_to_passage_down,
            'p': self.draw_path_from_up_to_down,
            'r': self.toggle_path_heuristic_cross,
            'v': self.show_map,
            'x': self.ascend_to_surface,
            'y': self.toggle_log_keycodes,
            'X': self.descend_to_end,
        }

    def print_user_input(self):
        self.io.msg(self.io.get_str("Tulostetaas tää: "))

    def update_without_acting(self):
        self.actions._do_action(0)
        return feedback(Action.Generic)

    def ask_action(self):
        c = self.io.get_key("Avail cmds: " + "".join(sorted(self.action_funcs.keys())))

        if c in self.action_funcs:
            self.action_funcs[c]()
            return feedback(Action.Debug)
        else:
            self.io.msg("Undefined debug key: {}".format(c))

    def add_monster(self):
        if self.level.creature_spawning_enabled:
            self.level.spawn_creature(self.level.creature_spawner.random_creature())
            self.update_without_acting()
        else:
            self.io.msg("No random spawning on this level. Can't add monster.")

    def show_map(self):
        Debug.show_map = not Debug.show_map
        self.actions.redraw()
        self.io.msg("Show map set to {}".format(Debug.show_map))

    def toggle_path_heuristic_cross(self):
        Debug.cross = not Debug.cross
        self.io.msg("Path heuristic cross set to {}".format(Debug.cross))

    def cycle_level_type(self):
        last_level_type = "All levels are already generated"
        for level in self.world.levels.values():
            if level.is_finalized:
                continue
            if level.generation_type == LevelGen.Dungeon:
                level.generation_type = LevelGen.Arena
            elif level.generation_type == LevelGen.Arena:
                level.generation_type = LevelGen.Dungeon
            last_level_type = level.generation_type
        self.io.msg("Level type set to {}".format(last_level_type))

    def show_path_debug(self):
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

    def kill_creatures_in_level(self):
        creature_list = list(self.level.creatures.values())
        creature_list.remove(self.creature)
        for i in creature_list:
            self.level.remove_creature(i)
        self.update_without_acting()
        self.io.msg("Abracadabra.")

    def draw_path_to_passage_down(self):
        passage_down_coord = self.level.get_location_coord(LevelLocation.Passage_Down)
        self.io.draw_path(self.level.path(self.creature.coord, passage_down_coord))
        self.actions.redraw()

    def draw_path_from_up_to_down(self):
        passage_up_coord = self.level.get_location_coord(LevelLocation.Passage_Up)
        passage_down_coord = self.level.get_location_coord(LevelLocation.Passage_Down)
        self.io.draw_path(self.level.path(passage_up_coord, passage_down_coord))
        self.actions.redraw()

    def interactive_console(self):
        self.io.suspend()
        game = self.actions.game
        io = self.io
        player = self.creature
        level = self.level
        code.interact(local=locals())
        self.io.resume()

    def toggle_log_keycodes(self):
        Debug.show_keycodes = not Debug.show_keycodes
        self.io.msg("Input code debug set to {}".format(Debug.show_keycodes))

    def display_curses_color_info(self):
        import curses
        self.io.msg("Colors: {} Pairs: {} Can change color? {}".format(
            curses.COLORS, curses.COLOR_PAIRS, "yes" if curses.can_change_color() else "no"))

    def print_message_debug_string(self):
        self.io.msg(Debug.debug_string)

    def sight_change(self, amount):
        self.creature.base_perception += amount
        return self.update_without_acting()

    def teleport_to_location(self, location):
        try:
            new_coord = self.level.get_location_coord(location)
        except KeyError:
            self.io.msg("This level doesn't seem to have a {} location".format(location))
            return
        if not self.level.is_passable(new_coord):
            self.level.remove_creature(self.level.creatures[new_coord])
        return self.actions.teleport(new_coord)

    def descend_to_end(self):
        self.io.prepared_input.extend([Binds.Descend.key] * 200)

    def ascend_to_surface(self):
        self.io.prepared_input.extend([Binds.Ascend.key] * 200)
