from __future__ import absolute_import, division, print_function, unicode_literals

import code
from config.debug import Debug
from level_template import LevelTemplate
from rdg import LevelGen
from level import LevelLocation


class DebugAction(object):

    def __init__(self, user_controller):
        self.user_controller = user_controller
        self.actions = {
            'v': self.show_map,
            'r': self.toggle_path_heuristic_cross,
            'l': self.cycle_level_type,
            'd': self.show_path_debug,
            'k': self.kill_creatures_in_level,
            'o': self.draw_path_to_passage_down,
            'p': self.draw_path_from_up_to_down,
            'i': self.interactive_console,
            'y': self.toggle_log_keycodes,
            'c': self.display_curses_color_info,
            'm': self.print_message_debug_string,
        }

    @property
    def creature(self):
        return self.user_controller.creature

    @property
    def level(self):
        return self.user_controller.game_actions.creature.level

    @property
    def game(self):
        return self.user_controller.game_actions.game

    @property
    def io(self):
        return self.user_controller.io

    @property
    def game_actions(self):
        return self.user_controller.game_actions

    def ask_action(self):
        c = self.io.get_key("Avail cmds: " + "".join(sorted(self.actions.keys())))

        if c in self.actions:
            self.actions[c]()
        else:
            self.io.msg("Undefined debug key: {}".format(c))

    def show_map(self):
        Debug.show_map = not Debug.show_map
        self.game_actions.redraw()
        self.io.msg("Show map set to {}".format(Debug.show_map))

    def toggle_path_heuristic_cross(self):
        Debug.cross = not Debug.cross
        self.io.msg("Path heuristic cross set to {}".format(Debug.cross))

    def cycle_level_type(self):
        if LevelTemplate.default_level_type == LevelGen.Dungeon:
            LevelTemplate.default_level_type = LevelGen.Arena
        else:
            LevelTemplate.default_level_type = LevelGen.Dungeon
        self.io.msg("Level type set to {}".format(LevelTemplate.default_level_type))

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
        self.io.msg("Abrakadabra.")

    def draw_path_to_passage_down(self):
        passage_down = self.level.get_location_coord(LevelLocation.Passage_Down)
        self.io.draw_path(self.level.path(self.creature.coord, passage_down))
        self.game_actions.redraw()

    def draw_path_from_up_to_down(self):
        passage_up = self.level.get_location_coord(LevelLocation.Passage_Up)
        passage_down = self.level.get_location_coord(LevelLocation.Passage_Down)
        self.io.draw_path(self.level.path(passage_up, passage_down))
        self.game_actions.redraw()

    def interactive_console(self):
        game = self.game
        self.io.suspend()
        code.interact(local=locals())
        self.io.resume()

    def toggle_log_keycodes(self):
        Debug.show_keycodes = not Debug.show_keycodes
        self.io.msg("Input code debug set to {}".format(Debug.show_keycodes))

    def display_curses_color_info(self):
        import curses
        self.io.msg(curses.COLORS, curses.COLOR_PAIRS, curses.can_change_color())
        self.io.msg(curses.A_ALTCHARSET, curses.A_BLINK, curses.A_BOLD, curses.A_DIM, curses.A_NORMAL,
            curses.A_REVERSE, curses.A_STANDOUT, curses.A_UNDERLINE)

    def print_message_debug_string(self):
        self.io.msg(Debug.debug_string)

    def sight_change(self, amount):
        self.creature.base_perception += amount
        self.game.update_view(self.creature)
        self.game_actions.redraw()

    def teleport_to_location(self, location):
        try:
            new_coord = self.level.get_location_coord(location)
        except KeyError:
            self.io.msg("This level doesn't seem to have a {} location".format(location))
            return
        if not self.level.is_passable(new_coord):
            self.level.remove_creature(self.level.get_creature(new_coord))
        return self.game_actions.teleport(new_coord)
