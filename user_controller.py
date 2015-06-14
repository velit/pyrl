from __future__ import absolute_import, division, print_function, unicode_literals

from functools import partial

from config.bindings import Bind
from enums.colors import Color, Pair
from enums.directions import Dir
from enums.keys import Key
from game_actions import ActionError
from generic_algorithms import add_vector
from interface.debug_action import DebugAction
from interface.help_screen import help_screen
from interface.inventory import equipment
from interface.walk_mode import WalkMode
from level import LevelLocation
from config.game import GameConf


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
        self.io = io_system
        self.walk_mode = WalkMode(self)
        self.debug_action = DebugAction(self)
        self.set_actions()

    @property
    def creature(self):
        return self.game_actions.creature

    def set_actions(self):
        self.actions = {
            'd':                  self.debug_action.ask_action,
            '+':                  partial(self.debug_action.sight_change, 1),
            '-':                  partial(self.debug_action.sight_change, -1),
            Key.CLOSE_WINDOW:     self.quit,
            Bind.Quit.key:        self.quit,
            Bind.Save.key:        self.save,
            Bind.Attack.key:      self.attack,
            Bind.Redraw.key:      self.redraw,
            Bind.History.key:     self.print_history,
            Bind.Look_Mode.key:   self.look,
            Bind.Help.key:        self.help_screen,
            Bind.Inventory.key:   self.equipment,
            Bind.Walk_Mode.key:   self.init_walk_mode,
            Bind.Show_Vision.key: self.show_vision,
            Bind.Ascend.key:      partial(self.ascend),
            Bind.Descend.key:     partial(self.descend),
        }
        for key, direction in Bind.action_direction.items():
            self.actions[key] = partial(self.act_to_dir, direction)
        for key, direction in Bind.walk_mode_direction.items():
            self.actions[key] = partial(self.init_walk_mode, direction)

    def get_user_input_and_act(self):
        while True:
            if self.walk_mode.is_walk_mode_active():
                error = self.walk_mode.continue_walk()
            else:
                key = self.io.get_key()
                if key not in self.actions:
                    self.io.msg("Undefined key: {}".format(key))
                    continue

                error = self.actions[key]()

            if error is not None:
                assert error != ActionError.AlreadyActed, "Player attempted to act twice."
                assert error != ActionError.PlayerAction, "Player was denied a player only action."

                if error in self.error_messages:
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
            if level.is_legal(new_coord):
                coord = new_coord
            self.io.msg(level.look_information(coord))
            if drawline_flag:
                self.io.draw_line(self.creature.coord, coord, ("*", Pair.Yellow))
                self.io.draw_line(coord, self.creature.coord, ("*", Pair.Yellow))
                self.io.msg("LoS: {}".format(level.check_los(self.creature.coord, coord)))
            if coord != self.creature.coord:
                char = level.get_visible_char(coord)
                char = char[0], (Color.Black, Color.Green)
                self.io.draw_char(coord, char)
                self.io.draw_char(self.creature.coord, level.get_visible_char(self.creature.coord), reverse=True)
            c = self.io.get_key()
            self.game_actions.redraw()
            direction = Dir.Stay
            if c in Bind.action_direction:
                direction = Bind.action_direction[c]
            elif c == 'd':
                drawline_flag = not drawline_flag
            elif c == 'b':
                from generic_algorithms import bresenham
                for coord in bresenham(level.get_coord(self.creature.coord), coord):
                    self.io.msg(coord)
            elif c == 's':
                if level.has_creature(coord):
                    self.game_actions.game.register_status_texts(level.get_creature(coord))
            elif c in Bind.Cancel or c in Bind.Look_Mode:
                break

    def quit(self):
        self.game_actions.quit()

    def save(self):
        self.game_actions.save()

    def attack(self):
        msg = "Specify attack direction, {} to abort".format(Bind.Cancel.key)
        key = self.io.ask(msg, Bind.action_direction.keys() | set(Bind.Cancel))
        if key in Bind.action_direction:
            return self.game_actions.attack(Bind.action_direction[key])

    def redraw(self):
        self.game_actions.redraw()

    def descend(self):
        coord = self.creature.coord
        level = self.creature.level
        if level.has_location(coord):
            location = level.get_location(coord)
            if location == LevelLocation.Passage_Up:
                #return "Cannot descend an upwards passage."
                return self.debug_action.teleport_to_location(LevelLocation.Passage_Down)
        else:
            #return "You don't find any downwards passage."
            return self.debug_action.teleport_to_location(LevelLocation.Passage_Down)

        return self.game_actions.enter_passage()

    def ascend(self):
        coord = self.creature.coord
        level = self.creature.level
        if level.has_location(coord):
            location = level.get_location(coord)
            if location != LevelLocation.Passage_Up:
                #return "Cannot ascend a downwards passage."
                return self.debug_action.teleport_to_location(LevelLocation.Passage_Up)
        else:
            #return "You don't find any upwards passage."
            return self.debug_action.teleport_to_location(LevelLocation.Passage_Up)

        return self.game_actions.enter_passage()

    def show_vision(self):
        GameConf.clearly_show_vision = not GameConf.clearly_show_vision
        self.game_actions.redraw()

    def print_history(self):
        self.io.message_bar.print_history()

    def equipment(self):
        return equipment(self.io, self.creature.equipment)

    def init_walk_mode(self, instant_direction=None):
        return self.walk_mode.init_walk_mode(instant_direction)

    def help_screen(self):
        help_screen(self.io)
        self.game_actions.redraw()
