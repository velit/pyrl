from __future__ import absolute_import, division, print_function, unicode_literals

import code
from functools import partial

from .inventory import equipment
from .walk_mode import WalkMode
from config.debug import Debug
from config.mappings import Mapping
from enums.colors import Color, Pair
from enums.directions import Dir
from enums.keys import Key
from game_actions import ActionError
from generic_algorithms import add_vector
from level_template import LevelTemplate, LevelLocation
from rdg import GenLevelType


class UserController(object):
    error_messages = {
        ActionError.AlreadyActed:         "You already acted.",
        ActionError.IllegalMove:          "You can't move there.",
        ActionError.IllegalTeleport:      "You can't teleport there.",
        ActionError.SwapTargetResists:    "The creature resists your swap attempt.",
        ActionError.NoSwapTarget:         "There isn't a creature there to swap with.",
        ActionError.PassageLeadsNoWhere:  "This passage doesn't seem to lead anywhere.",
        ActionError.NoPassage:            "This location doesn't have a passage.",
        ActionError.PlayerAction:         "Only the player can do this action.",
    }

    def __init__(self, game_actions, io_system):
        self.game_actions = game_actions
        self.creature = game_actions.creature
        self.io = io_system
        self.walk_mode = WalkMode(self)
        self.action_mapping = {
            'd':  self.debug_action,
            '+':  partial(self.sight_change, 1),
            '-':  partial(self.sight_change, -1),

            Key.CLOSE_WINDOW:   self.quit,
            Mapping.Quit:       self.quit,
            Mapping.Save:       self.save,
            Mapping.Attack:     self.attack,
            Mapping.Redraw:     self.redraw,
            Mapping.History:    self.print_history,
            Mapping.Look_Mode:  self.look,
            Mapping.Help:       self.help_screen,
            Mapping.Inventory:  self.equipment,
            Mapping.Walk_Mode:  self.init_walk_mode,
            Mapping.Ascend:     partial(self.enter, LevelLocation.Passage_Up),
            Mapping.Descend:    partial(self.enter, LevelLocation.Passage_Down),
        }
        for key, direction in Mapping.Directions.items():
            self.action_mapping[key] = partial(self.act_to_dir, direction)
        for key, direction in Mapping.Instant_Walk_Mode.items():
            self.action_mapping[key] = partial(self.init_walk_mode, direction)

    def get_user_input_and_act(self):
        while True:
            if self.walk_mode.is_walk_mode_active():
                error = self.walk_mode.continue_walk()
            else:
                key = self.io.get_key()
                if key not in self.action_mapping:
                    self.io.msg("Undefined key: {}".format(key))
                    continue

                error = self.action_mapping[key]()

            if error is not None:
                if error == ActionError.AlreadyActed:
                    raise AssertionError("Player attempted to act twice.")
                elif error == ActionError.PlayerAction:
                    raise AssertionError("Player was denied a player only action.")
                elif error in self.error_messages:
                    self.io.msg(self.error_messages[error])
                else:
                    self.io.msg(error)

            if self.game_actions.already_acted():
                return

    def act_to_dir(self, direction):
        target_coord = add_vector(self.creature.coord, direction)
        level = self.creature.level
        error = None
        if level.creature_can_move(self.creature, direction):
            error = self.game_actions.move(direction)
        elif level.has_creature(target_coord):
            error = self.game_actions.attack(direction)
        else:
            error = ActionError.IllegalMove
        return error

    def look(self):
        coord = self.creature.coord
        level = self.creature.level
        drawline_flag = False
        direction = Dir.Stay
        while True:
            new_coord = add_vector(coord, direction)
            if level.legal_coord(new_coord):
                coord = new_coord
            self.io.msg(level.look_information(coord))
            if drawline_flag:
                self.io.draw_line(self.creature.coord, coord, ("*", Pair.Yellow))
                self.io.draw_line(coord, self.creature.coord, ("*", Pair.Yellow))
                self.io.msg("LoS: {}".format(level.check_los(self.creature.coord, coord)))
            if coord != self.creature.coord:
                char = level._get_visible_char(coord)
                char = char[0], (Color.Black, Color.Green)
                self.io.draw_char(coord, char)
                self.io.draw_char(self.creature.coord, level._get_visible_char(self.creature.coord), reverse=True)
            c = self.io.get_key()
            self.game_actions.redraw()
            direction = Dir.Stay
            if c in Mapping.Directions:
                direction = Mapping.Directions[c]
            elif c == 'd':
                drawline_flag = not drawline_flag
            elif c == 'b':
                from generic_algorithms import bresenham
                for coord in bresenham(level.get_coord(self.creature.coord), coord):
                    self.io.msg(coord)
            elif c == 's':
                if level.has_creature(coord):
                    self.game_actions.game.register_status_texts(level.get_creature(coord))
            elif c in Mapping.Group_Cancel or c == Mapping.Look_Mode:
                break

    def quit(self):
        self.game_actions.quit()

    def save(self):
        self.game_actions.save()

    def attack(self):
        msg = "Specify attack direction, {} to abort".format(Mapping.Cancel)
        key = self.io.ask(msg, Mapping.Directions.keys() | Mapping.Group_Cancel)
        if key in Mapping.Directions:
            return self.game_actions.attack(Mapping.Directions[key])

    def redraw(self):
        self.game_actions.redraw()

    def enter(self, passage):
        coord = self.creature.coord
        level = self.creature.level
        if level.is_exit(coord) and level.get_exit(coord) == passage:
            return self.game_actions.enter_passage()
        else:
            # debug use
            try:
                new_coord = level.get_passage_coord(passage)
            except KeyError:
                self.io.msg("This level doesn't seem to have a passage that way.")
            else:
                if not level.is_passable(new_coord):
                    level.remove_creature(level.get_creature(new_coord))
                error = self.game_actions.teleport(new_coord)
                return error

    def sight_change(self, amount):
        self.creature.base_perception += amount

    def print_history(self):
        self.io.m.print_history()

    def debug_action(self):
        level = self.creature.level

        def show_map():
            Debug.show_map = not Debug.show_map
            self.game_actions.redraw()
            self.io.msg("Show map set to {}".format(Debug.show_map))

        def toggle_path_heuristic_cross():
            Debug.cross = not Debug.cross
            self.io.msg("Path heuristic cross set to {}".format(Debug.cross))

        def cycle_level_type():
            if LevelTemplate.default_level_type == GenLevelType.Dungeon:
                LevelTemplate.default_level_type = GenLevelType.Arena
            else:
                LevelTemplate.default_level_type = GenLevelType.Dungeon
            self.io.msg("Level type set to {}".format(LevelTemplate.default_level_type))

        def show_path_debug():
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

        def show_fov_debug():
            Debug.reverse = not Debug.reverse
            self.game_actions.redraw()
            self.io.msg("Reverse set to {}".format(Debug.reverse))

        def kill_creatures_in_level():
            creature_list = list(level.creatures.values())
            creature_list.remove(self.creature)
            for i in creature_list:
                level.remove_creature(i)
            self.io.msg("Abrakadabra.")

        def draw_path_to_passage_down():
            passage_down = level.get_passage_coord(LevelLocation.Passage_Down)
            self.io.draw_path(level.path(self.creature.coord, passage_down))
            self.game_actions.redraw()

        def draw_path_from_up_to_down():
            passage_up = level.get_passage_coord(LevelLocation.Passage_Up)
            passage_down = level.get_passage_coord(LevelLocation.Passage_Down)
            self.io.draw_path(level.path(passage_up, passage_down))
            self.game_actions.redraw()

        def interactive_console():
            self.io.suspend()
            code.interact(local=locals())
            self.io.resume()

        def toggle_log_keycodes():
            Debug.show_keycodes = not Debug.show_keycodes
            self.io.msg("Input code debug set to {}".format(Debug.show_keycodes))

        def display_curses_color_info():
            import curses
            self.io.msg(curses.COLORS, curses.COLOR_PAIRS, curses.can_change_color())
            self.io.msg(curses.A_ALTCHARSET, curses.A_BLINK, curses.A_BOLD, curses.A_DIM, curses.A_NORMAL,
                curses.A_REVERSE, curses.A_STANDOUT, curses.A_UNDERLINE)

        def print_message_debug_string():
            self.io.msg(Debug.debug_string)

        debug_actions = {
            'v': show_map,
            'r': toggle_path_heuristic_cross,
            'l': cycle_level_type,
            'd': show_path_debug,
            'h': show_fov_debug,
            'k': kill_creatures_in_level,
            'o': draw_path_to_passage_down,
            'p': draw_path_from_up_to_down,
            'i': interactive_console,
            'y': toggle_log_keycodes,
            'c': display_curses_color_info,
            'm': print_message_debug_string,
        }
        c = self.io.get_key("Avail cmds: " + "".join(sorted(debug_actions.keys())))

        if c in debug_actions:
            debug_actions[c]()
        else:
            self.io.msg("Undefined debug key: {}".format(c))

    def equipment(self):
        return equipment(self.io, self.creature.equipment)

    def init_walk_mode(self, instant_direction=None):
        return self.walk_mode.init_walk_mode(instant_direction)

    def help_screen(self):
        header = "Help Screen, ^ means ctrl, ! means alt"
        help_lines = [
            "Help           {0}".format(Mapping.Help),
            "Look Mode      {0}".format(Mapping.Look_Mode),
            "Inventory      {0}".format(Mapping.Inventory),
            "Descend        {0}".format(Mapping.Descend),
            "Ascend         {0}".format(Mapping.Ascend),
            "Quit           {0}".format(Mapping.Quit),
            "Save           {0}".format(Mapping.Save),
            "Manual Attack  {0}".format(Mapping.Attack),
            "Redraw Screen  {0}".format(Mapping.Redraw),
            "Print History  {0}".format(Mapping.History),
            "Walk Mode      {0}".format(Mapping.Walk_Mode),
            "",
            "Direction keys used for movement, implicit attacking, walk mode, etc:",
            "  Numpad keys",
            "  So called vi-keys (hjklyubn.)",
            "",
            "Debug keys that start with d",
            "Map hax             dv        Other path                   dp",
            "Kill monsters       dk        Reverse fov                  dh",
            "Path to stairs      do        Interactive console          di",
            "Toggle path debugs  dd        Change level types           dl",
            "Print debug string  dm        Set cross heuristic in path  dr",
            "",
            "Colors available     dc (only on ncurses ie. pyrl.py)",
        ]
        footer = "{0} to close".format(Mapping.Cancel)
        self.io.menu(header, help_lines, footer, Mapping.Group_Cancel)
        self.game_actions.redraw()
