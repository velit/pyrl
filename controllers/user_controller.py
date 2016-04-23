from __future__ import absolute_import, division, print_function, unicode_literals

from functools import partial

import interface.inventory
from config.bindings import Bind
from enums.colors import Color, Pair
from enums.directions import Dir
from enums.keys import Key
from game_actions import ActionError, Action, GameActionsProperties
from generic_algorithms import add_vector
from interface.help_screen import help_screen
from world.level import LevelLocation
from config.game import GameConf


class UserController(GameActionsProperties, object):

    error_messages = {
        ActionError.IllegalMove:          "You can't move there.",
        ActionError.IllegalTeleport:      "You can't teleport there.",
        ActionError.SwapTargetResists:    "The creature resists your swap attempt.",
        ActionError.NoSwapTarget:         "There isn't a creature there to swap with.",
        ActionError.PassageLeadsNoWhere:  "This passage doesn't seem to lead anywhere.",
        ActionError.NoPassage:            "This location doesn't have a passage.",
        ActionError.NoItemsOnGround:      "There aren't any items here to pick up.",
    }

    def __init__(self, game_actions):
        self.actions = game_actions

        from controllers.walk_mode import WalkMode
        self.walk_mode = WalkMode(self.actions)

        from controllers.debug_action import DebugAction
        self.debug_action = DebugAction(self.actions)

        self.set_actions()

    def set_actions(self):
        self.actions_funcs = {
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
                self.actions_funcs[key] = action

    def _act(self):
        if self.walk_mode.is_walk_mode_active():
            feedback = self.walk_mode.continue_walk()
        else:
            key = self.io.get_key()
            if key in self.actions_funcs:
                feedback = self.actions_funcs[key]()
            else:
                self.io.msg("Undefined key: {}".format(key))
                feedback = None

        if feedback is None:
            assert not self.actions.already_acted(), \
                "Player did something but user_controller got no feedback from the game from it."

        return feedback

    def act(self):
        while True:
            feedback = self._act()
            if feedback is None and not self.actions.already_acted():
                continue

            assert feedback.type != ActionError.AlreadyActed, "Player attempted to act twice."
            assert feedback.type != ActionError.PlayerAction, "Player was denied a player only action."

            if feedback.type in ActionError:
                if feedback.type in self.error_messages:
                    self.io.msg(self.error_messages[feedback.type])
                else:
                    self.io.msg(feedback.type, feedback.params)
            elif feedback.type in (Action.Move, Action.Teleport, Action.Swap, Action.Spawn):
                items = self.actions.view_floor_items()

                if self.actions.get_passage():
                    self.io.msg("There is a {} here.".format(self.actions.get_tile().name))

                if len(items) == 1:
                    self.io.msg("A {} is lying here.".format(items[0].name))
                elif 1 < len(items) <= 10:
                    self.io.msg("There are several items lying here.")
                elif 10 < len(items):
                    self.io.msg("There is a stack of items lying here.")

            if self.actions.already_acted():
                return

    def act_to_dir(self, direction):
        return self.actions.act_to_dir(direction)

    def wait(self):
        return self.actions.wait()

    def look(self):
        coord = self.coord
        drawline_flag = False
        direction = Dir.Stay
        while True:
            new_coord = add_vector(coord, direction)
            if self.actions.level.is_legal(new_coord):
                coord = new_coord
            self.io.msg(self.actions.level.look_information(coord))
            if drawline_flag:
                self.io.draw_line(self.coord, coord, ("*", Pair.Yellow))
                self.io.draw_line(coord, self.coord, ("*", Pair.Yellow))
                self.io.msg("LoS: {}".format(self.actions.level.check_los(self.coord, coord)))
            if coord != self.coord:
                char = self.actions.level.visible_char(coord)
                char = char[0], (Color.Black, Color.Green)
                self.io.draw_char(coord, char)
                self.io.draw_char(self.coord, self.actions.level.visible_char(self.coord), reverse=True)
            c = self.io.get_key()
            self.actions.redraw()
            direction = Dir.Stay
            if c in Bind.action_direction:
                direction = Bind.action_direction[c]
            elif c == 'd':
                drawline_flag = not drawline_flag
            elif c == 'b':
                from generic_algorithms import bresenham
                for coord in bresenham(self.actions.level.get_coord(self.coord), coord):
                    self.io.msg(coord)
            elif c == 's':
                if coord in self.actions.level.creatures:
                    self.actions.game.register_status_texts(self.actions.level.creatures[coord])
            elif c in Bind.Cancel or c in Bind.Look_Mode:
                break

    def quit(self):
        self.actions.quit()

    def save(self):
        self.actions.save()

    def attack(self):
        msg = "Specify attack direction, {} to abort".format(Bind.Cancel.key)
        key = self.io.ask(msg, Bind.action_direction.keys() | set(Bind.Cancel))
        if key in Bind.action_direction:
            return self.actions.attack(Bind.action_direction[key])

    def redraw(self):
        self.actions.redraw()

    def descend(self):
        location = self.actions.get_passage()
        if location not in (None, LevelLocation.Passage_Up):
            return self.actions.enter_passage()
        else:
            return self.debug_action.teleport_to_location(LevelLocation.Passage_Down)
            #return "You don't find any downwards passage."

    def ascend(self):
        location = self.actions.get_passage()
        if location != LevelLocation.Passage_Up:
            return self.debug_action.teleport_to_location(LevelLocation.Passage_Up)
            #return "You don't find any upwards passage."
        else:
            return self.actions.enter_passage()

    def show_vision(self):
        GameConf.clearly_show_vision = not GameConf.clearly_show_vision
        self.actions.redraw()

    def print_history(self):
        self.io.message_bar.print_history()

    def equipment(self):
        return interface.inventory.equipment(self.actions)

    def backpack(self):
        return interface.inventory.backpack(self.actions)

    def pickup_items(self):
        return interface.inventory.pickup_items(self.actions)

    def drop_items(self):
        return interface.inventory.drop_items(self.actions)

    def init_walk_mode(self, instant_direction=None):
        return self.walk_mode.init_walk_mode(instant_direction)

    def help_screen(self):
        help_screen(self.io)
        self.actions.redraw()
