from __future__ import absolute_import, division, print_function, unicode_literals

from functools import partial

import interface.inventory
from config.bindings import Bind
from enums.colors import Color, Pair
from enums.directions import Dir
from enums.keys import Key
from game_actions import ActionFeedback
from generic_algorithms import add_vector
from interface.help_screen import help_screen
from world.level import LevelLocation
from config.game import GameConf


class UserController(object):
    error_messages = {
        ActionFeedback.IllegalMove:          "You can't move there.",
        ActionFeedback.IllegalTeleport:      "You can't teleport there.",
        ActionFeedback.SwapTargetResists:    "The creature resists your swap attempt.",
        ActionFeedback.NoSwapTarget:         "There isn't a creature there to swap with.",
        ActionFeedback.PassageLeadsNoWhere:  "This passage doesn't seem to lead anywhere.",
        ActionFeedback.NoPassage:            "This location doesn't have a passage.",
        ActionFeedback.NoItemsOnGround:      "There aren't any items on the ground to pick up.",
    }

    def __init__(self, game_actions):
        from controllers.debug_action import DebugAction
        from controllers.walk_mode import WalkMode

        self.game_actions = game_actions
        self.walk_mode = WalkMode(self.game_actions)
        self.debug_action = DebugAction(self.game_actions)
        self.set_actions()

    @property
    def creature(self):
        return self.game_actions.creature

    @property
    def coord(self):
        return self.game_actions.creature.coord

    @property
    def io(self):
        return self.game_actions.io

    def set_actions(self):
        self.actions = {
            '+':                     partial(self.debug_action.sight_change, 1),
            '-':                     partial(self.debug_action.sight_change, -1),
            Key.CLOSE_WINDOW:        self.quit,
        }

        unfinalized_actions = {
            Bind.Debug_Commands:     self.debug_action.ask_action,
            Bind.Quit:               self.quit,
            Bind.Save:               self.save,
            Bind.Attack:             self.attack,
            Bind.Redraw:             self.redraw,
            Bind.History:            self.print_history,
            Bind.Look_Mode:          self.look,
            Bind.Help:               self.help_screen,
            Bind.Equipment:          self.equipment,
            Bind.Backpack:           self.backpack,
            Bind.Pick_Up_Items:      self.pickup_items,
            Bind.Drop_Items:         self.drop_items,
            Bind.Walk_Mode:          self.init_walk_mode,
            Bind.Show_Vision:        self.show_vision,
            Bind.Ascend:             self.ascend,
            Bind.Descend:            self.descend,

            Bind.SouthWest:          partial(self.act_to_dir, Dir.SouthWest),
            Bind.South:              partial(self.act_to_dir, Dir.South),
            Bind.SouthEast:          partial(self.act_to_dir, Dir.SouthEast),
            Bind.West:               partial(self.act_to_dir, Dir.West),
            Bind.Stay:               self.wait,
            Bind.East:               partial(self.act_to_dir, Dir.East),
            Bind.NorthWest:          partial(self.act_to_dir, Dir.NorthWest),
            Bind.North:              partial(self.act_to_dir, Dir.North),
            Bind.NorthEast:          partial(self.act_to_dir, Dir.NorthEast),

            Bind.Instant_SouthWest:  partial(self.init_walk_mode, Dir.SouthWest),
            Bind.Instant_South:      partial(self.init_walk_mode, Dir.South),
            Bind.Instant_SouthEast:  partial(self.init_walk_mode, Dir.SouthEast),
            Bind.Instant_West:       partial(self.init_walk_mode, Dir.West),
            Bind.Instant_Stay:       partial(self.init_walk_mode, Dir.Stay),
            Bind.Instant_East:       partial(self.init_walk_mode, Dir.East),
            Bind.Instant_NorthWest:  partial(self.init_walk_mode, Dir.NorthWest),
            Bind.Instant_North:      partial(self.init_walk_mode, Dir.North),
            Bind.Instant_NorthEast:  partial(self.init_walk_mode, Dir.NorthEast),
        }

        for keys, action in unfinalized_actions.items():
            for key in keys:
                self.actions[key] = action

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
                assert error != ActionFeedback.AlreadyActed, "Player attempted to act twice."
                assert error != ActionFeedback.PlayerAction, "Player was denied a player only action."

                if error in self.error_messages:
                    self.io.msg(self.error_messages[error])
                else:
                    self.io.msg(error)

            if self.game_actions.already_acted():
                return

    def act_to_dir(self, direction):
        return self.game_actions.act_to_dir(direction)

    def wait(self):
        return self.game_actions.wait()

    def look(self):
        coord = self.coord
        drawline_flag = False
        direction = Dir.Stay
        while True:
            new_coord = add_vector(coord, direction)
            if self.game_actions.level.is_legal(new_coord):
                coord = new_coord
            self.io.msg(self.game_actions.level.look_information(coord))
            if drawline_flag:
                self.io.draw_line(self.coord, coord, ("*", Pair.Yellow))
                self.io.draw_line(coord, self.coord, ("*", Pair.Yellow))
                self.io.msg("LoS: {}".format(self.game_actions.level.check_los(self.coord, coord)))
            if coord != self.coord:
                char = self.game_actions.level.visible_char(coord)
                char = char[0], (Color.Black, Color.Green)
                self.io.draw_char(coord, char)
                self.io.draw_char(self.coord, self.game_actions.level.visible_char(self.coord), reverse=True)
            c = self.io.get_key()
            self.game_actions.redraw()
            direction = Dir.Stay
            if c in Bind.action_direction:
                direction = Bind.action_direction[c]
            elif c == 'd':
                drawline_flag = not drawline_flag
            elif c == 'b':
                from generic_algorithms import bresenham
                for coord in bresenham(self.game_actions.level.get_coord(self.coord), coord):
                    self.io.msg(coord)
            elif c == 's':
                if coord in self.game_actions.level.creatures:
                    self.game_actions.game.register_status_texts(self.game_actions.level.creatures[coord])
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
        location = self.game_actions.get_passage()
        if location not in (ActionFeedback.NoPassage, LevelLocation.Passage_Up):
            return self.game_actions.enter_passage()
        else:
            return self.debug_action.teleport_to_location(LevelLocation.Passage_Down)
            #return "You don't find any downwards passage."

    def ascend(self):
        location = self.game_actions.get_passage()
        if location != LevelLocation.Passage_Up:
            return self.debug_action.teleport_to_location(LevelLocation.Passage_Up)
            #return "You don't find any upwards passage."
        else:
            return self.game_actions.enter_passage()

    def show_vision(self):
        GameConf.clearly_show_vision = not GameConf.clearly_show_vision
        self.game_actions.redraw()

    def print_history(self):
        self.io.message_bar.print_history()

    def equipment(self):
        return interface.inventory.equipment(self.game_actions)

    def backpack(self):
        return interface.inventory.backpack(self.game_actions)

    def pickup_items(self):
        return interface.inventory.pickup_items(self.game_actions)

    def drop_items(self):
        return interface.inventory.drop_items(self.game_actions)

    def init_walk_mode(self, instant_direction=None):
        return self.walk_mode.init_walk_mode(instant_direction)

    def help_screen(self):
        help_screen(self.io)
        self.game_actions.redraw()
