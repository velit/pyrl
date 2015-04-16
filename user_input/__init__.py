from __future__ import absolute_import, division, print_function, unicode_literals

import code

from const.colors import Color, Pair
from const.directions import Dir
import const.game as GAME
import level_template
from mappings import Mapping
import rdg
from functools import partial
from .inventory import equipment
from .walk_mode import WalkMode
from config import debug
from const.keys import Key
from generic_algorithms import add_vector


class UserInput(object):
    def __init__(self, game, creature, io_system):
        self.game = game
        self.creature = creature
        self.io = io_system
        self.walk_mode = WalkMode(self.game, self.creature, self.io)
        self.actions = {
            Key.CLOSE_WINDOW:   self.endgame,
            Mapping.Quit:       self.endgame,
            Mapping.Save:       self.savegame,
            Mapping.Attack:     self.attack,
            Mapping.Redraw:     self.redraw,
            Mapping.History:    self.print_history,
            Mapping.Look_Mode:  self.look,
            Mapping.Help:       self.help_screen,
            Mapping.Inventory:  self.equipment,
            Mapping.Walk_Mode:  self.init_walk_mode,
            Mapping.Ascend:     partial(self.enter, GAME.PASSAGE_UP),
            Mapping.Descend:    partial(self.enter, GAME.PASSAGE_DOWN),

            'd':  self.debug_action,
            '+':  partial(self.sight_change, 1),
            '-':  partial(self.sight_change, -1),
        }
        for key, direction in Mapping.Directions.items():
            self.actions[key] = partial(self.act_to_dir, direction)
        for key, direction in Mapping.Instant_Walk_Mode.items():
            self.actions[key] = partial(self.init_walk_mode, direction)

    def get_user_input_and_act(self):
        while self.creature.can_act():
            if self.walk_mode.is_walk_mode_active():
                self.walk_mode.continue_walk()
            else:
                key = self.io.get_key()
                if key in self.actions:
                    action_not_free = self.actions[key]
                    if action_not_free():
                        return
                else:
                    self.io.msg("Undefined key: {}".format(key))

    def act_to_dir(self, direction):
        target_coord = add_vector(self.creature.coord, direction)
        level = self.creature.level
        if level.creature_can_move(self.creature, direction):
            self.game.creature_move(self.creature, direction)
        elif level.has_creature(target_coord):
            self.game.creature_attack(self.creature, direction)
        elif not self.creature.can_act():
            self.io.msg("You're out of energy.")
        else:
            self.io.msg("You can't move there.")

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
            self.game.redraw()
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
                    self.game.register_status_texts(level.get_creature(coord))
            elif c in Mapping.Group_Cancel or c == Mapping.Look_Mode:
                break

    def endgame(self, *a, **k):
        self.game.endgame(*a, **k)

    def savegame(self, *a, **k):
        self.game.savegame(*a, **k)

    def attack(self):
        msg = "Specify attack direction, {} to abort".format(Mapping.Cancel)
        key = self.io.ask(msg, Mapping.Directions.keys() | Mapping.Group_Cancel)
        if key in Mapping.Directions:
            self.game.creature_attack(self.creature, Mapping.Directions[key])

    def redraw(self):
        self.game.redraw()

    def enter(self, passage):
        coord = self.game.player.coord
        level = self.creature.level
        if level.is_exit(coord) and level.get_exit(coord) == passage:
            self.game.creature_enter_passage(self.creature)
        else:
            try:
                new_coord = level.get_passage_coord(passage)
            except KeyError:
                self.io.msg("This level doesn't seem to have a corresponding passage.")
            else:
                if not level.is_passable(new_coord):
                    level.remove_creature(level.get_creature(new_coord))
                if not self.game.creature_teleport(self.creature, new_coord):
                    self.io.msg("Teleport failed.")

    def sight_change(self, amount):
        from const.slots import BODY
        from const.stats import SIGHT
        self.creature.get_item(BODY).stats[SIGHT] += amount
        return True

    def print_history(self):
        self.io.m.print_history()

    def debug_action(self):
        level = self.creature.level
        c = self.io.get_key("Avail cmds: bcdhikloprsvy+-")
        if c == 'v':
            debug.show_map = not debug.show_map
            self.game.redraw()
            self.io.msg("Show map set to {}".format(debug.show_map))
        elif c == 'r':
            debug.cross = not debug.cross
            self.io.msg("Path heuristic cross set to {}".format(debug.cross))
        elif c == 'l':
            level_template.DEFAULT_LEVEL_TYPE = rdg.ARENA if level_template.DEFAULT_LEVEL_TYPE == rdg.DUNGEON else rdg.DUNGEON
            self.io.msg("Level type set to {}".format(level_template.DEFAULT_LEVEL_TYPE))
        elif c == 'd':
            if not debug.path:
                debug.path = True
                self.io.msg("Path debug set")
            elif not debug.path_step:
                debug.path_step = True
                self.io.msg("Path debug and stepping set")
            else:
                debug.path = False
                debug.path_step = False
                self.io.msg("Path debug unset")
        elif c == 'h':
            debug.reverse = not debug.reverse
            self.game.redraw()
            self.io.msg("Reverse set to {}".format(debug.reverse))
        elif c == 'k':
            creature_list = level.creatures.values()
            creature_list.remove(self.creature)
            for i in creature_list:
                level.remove_creature(i)
            self.io.msg("Abrakadabra.")
            return True
        elif c == 'o':
            passage_down = level.get_passage_coord(GAME.PASSAGE_DOWN)
            self.io.draw_path(level.path(self.creature.coord, passage_down))
            self.game.redraw()
        elif c == 'p':
            passage_up = level.get_passage_coord(GAME.PASSAGE_UP)
            passage_down = level.get_passage_coord(GAME.PASSAGE_DOWN)
            self.io.draw_path(level.path(passage_up, passage_down))
            self.game.redraw()
        elif c == 'i':
            self.io.suspend()
            code.interact(local=locals())
            self.io.resume()
        elif c == 'y':
            debug.show_keycodes = not debug.show_keycodes
            self.io.msg("Input code debug set to {}".format(debug.show_keycodes))
        elif c == 'c':
            import curses
            self.io.msg(curses.COLORS, curses.COLOR_PAIRS, curses.can_change_color())
            self.io.msg(curses.A_ALTCHARSET, curses.A_BLINK, curses.A_BOLD, curses.A_DIM, curses.A_NORMAL,
                curses.A_REVERSE, curses.A_STANDOUT, curses.A_UNDERLINE)
        elif c == 'm':
            self.io.msg(debug.debug_string)
        else:
            self.io.msg("Undefined debug key: {}".format(chr(c) if 0 < c < 128 else c))

    def equipment(self):
        return equipment(self.io, self.game, self.creature)

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
        self.game.redraw()
