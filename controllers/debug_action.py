from __future__ import absolute_import, division, print_function, unicode_literals

import code
import random
from rdg import LevelGen
from config.debug import Debug
from config.bindings import Bind
from world.level import LevelLocation
from creature.creature import Creature
from game_actions import GameActionsProperties


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

    def ask_action(self):
        c = self.io.get_key("Avail cmds: " + "".join(sorted(self.action_funcs.keys())))

        if c in self.action_funcs:
            self.action_funcs[c]()
        else:
            self.io.msg("Undefined debug key: {}".format(c))

    def add_monster(self):
        if self.level.creature_spawn_list:
            self.level.spawn_creature(Creature(random.choice(self.level.creature_spawn_list)))
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
        for level_template in self.world.level_templates.values():
            if level_template.generation_type == LevelGen.Dungeon:
                level_template.generation_type = LevelGen.Arena
            elif level_template.generation_type == LevelGen.Arena:
                level_template.generation_type = LevelGen.Dungeon
            last_template_type = level_template.generation_type
        self.io.msg("Level type set to {}".format(last_template_type))

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
        self.io.msg("Abrakadabra.")

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
        self.io.msg(curses.COLORS, curses.COLOR_PAIRS, curses.can_change_color())
        self.io.msg(curses.A_ALTCHARSET, curses.A_BLINK, curses.A_BOLD, curses.A_DIM, curses.A_NORMAL,
            curses.A_REVERSE, curses.A_STANDOUT, curses.A_UNDERLINE)

    def print_message_debug_string(self):
        self.io.msg(Debug.debug_string)

    def sight_change(self, amount):
        self.creature.base_perception += amount
        self.update_without_acting()

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
        self.io.prepared_input.extend([Bind.Descend.key]*200)

    def ascend_to_surface(self):
        self.io.prepared_input.extend([Bind.Ascend.key]*200)
