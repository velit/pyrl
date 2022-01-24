from __future__ import annotations

import logging
from collections.abc import Callable
from functools import partial
from typing import Literal

from pyrl.functions.coord_algorithms import add_vector
from pyrl.config.binds import Binds
from pyrl.config.config import Config
from pyrl.creature.action import Action, ActionException
from pyrl.creature.game_actions import GameActions
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.structures.helper_mixins import CreatureActionsMixin
from pyrl.types.color import Color, ColorPairs
from pyrl.types.direction import Direction, Dir
from pyrl.types.keys import Keys, KeyTuple
from pyrl.user_interface.help_view import help_view
from pyrl.user_interface.inventory_views import equipment_view, backpack_view, pickup_items_view, drop_items_view
from pyrl.user_interface.lines_view import build_lines, lines_view

ActionCallable = Callable[[], Action]

class UserController(CreatureActionsMixin):

    def __init__(self, actions: GameActions) -> None:
        from pyrl.controllers.walk_mode import WalkMode
        from pyrl.controllers.debug_action import DebugAction
        self.actions = actions
        self.walk_mode = WalkMode(self.actions)
        self.debug_action = DebugAction(self.actions)
        self.action_lookup = self.define_actions()

    def define_actions(self) -> dict[str, ActionCallable]:
        actions_funcs: dict[str, ActionCallable] = {
            '+':                      partial(self.debug_action.sight_change, 1),
            '-':                      partial(self.debug_action.sight_change, -1),
            Keys.WINDOW_RESIZE:       self.redraw,
            Keys.CLOSE_WINDOW:        self.quit,
        }

        unfinalized_actions: dict[KeyTuple, ActionCallable] = {
            Binds.Debug_Commands:     self.debug_action.ask_action,
            Binds.Quit:               self.quit,
            Binds.Save:               self.save,
            Binds.Attack:             self.attack,
            Binds.Redraw:             self.redraw,
            Binds.History:            self.print_history,
            Binds.Look_Mode:          self.look,
            Binds.Help:               self.help_screen,
            Binds.Equipment:          self.manage_equipment,
            Binds.Backpack:           self.manage_backpack,
            Binds.Pick_Up_Items:      self.pickup_items,
            Binds.Drop_Items:         self.drop_items,
            Binds.Walk_Mode:          self.init_walk_mode,
            Binds.Show_Vision:        self.show_vision,
            Binds.Ascend:             self.ascend,
            Binds.Descend:            self.descend,
            Binds.Toggle_Fullscreen:  self.toggle_fullscreen,
            Binds.Next_Tileset:       self.next_tileset,
            Binds.Previous_Tileset:   self.previous_tileset,
            Binds.Next_Bdf:           self.next_bdf,
            Binds.Previous_Bdf:       self.previous_bdf,

            Binds.North:              partial(self.act_to_dir, Dir.North),
            Binds.NorthEast:          partial(self.act_to_dir, Dir.NorthEast),
            Binds.East:               partial(self.act_to_dir, Dir.East),
            Binds.SouthEast:          partial(self.act_to_dir, Dir.SouthEast),
            Binds.South:              partial(self.act_to_dir, Dir.South),
            Binds.SouthWest:          partial(self.act_to_dir, Dir.SouthWest),
            Binds.West:               partial(self.act_to_dir, Dir.West),
            Binds.NorthWest:          partial(self.act_to_dir, Dir.NorthWest),
            Binds.Stay:               self.wait,

            Binds.Instant_North:      partial(self.init_walk_mode, Dir.North),
            Binds.Instant_NorthEast:  partial(self.init_walk_mode, Dir.NorthEast),
            Binds.Instant_East:       partial(self.init_walk_mode, Dir.East),
            Binds.Instant_SouthEast:  partial(self.init_walk_mode, Dir.SouthEast),
            Binds.Instant_South:      partial(self.init_walk_mode, Dir.South),
            Binds.Instant_SouthWest:  partial(self.init_walk_mode, Dir.SouthWest),
            Binds.Instant_West:       partial(self.init_walk_mode, Dir.West),
            Binds.Instant_NorthWest:  partial(self.init_walk_mode, Dir.NorthWest),
            Binds.Instant_Stay:       partial(self.init_walk_mode, Dir.Stay),
        }

        for keys, action in unfinalized_actions.items():
            for key in keys:
                actions_funcs[key] = action

        return actions_funcs

    def act(self) -> Action:
        try:
            action = self._get_action()
        except ActionException as exception:
            self.io.msg(exception.player_message)
            action = Action.No_Action

        if action in (Action.Move, Action.Teleport, Action.Swap, Action.Spawn):
            items = self.actions.inspect_floor_items()

            if self.actions.get_passage():
                self.io.msg(f"There is a {self.actions.get_tile().name} here.")

            if len(items) == 1:
                self.io.msg(f"A {items[0].name} is lying here.")
            elif 1 < len(items) <= 10:
                self.io.msg("There are several items lying here.")
            elif 10 < len(items):
                self.io.msg("There is a stack of items lying here.")

        return action

    def _get_action(self) -> Action:
        action: Action
        if self.walk_mode.active:
            action = self.walk_mode.continue_walk()
        else:
            key = self.io.get_key()
            if key in self.action_lookup:
                action = self.action_lookup[key]()
            else:
                self.io.msg(f"Undefined key: {key}")
                action = Action.No_Action

        return action

    def act_to_dir(self, direction: Direction) -> Literal[Action.Move] | Literal[Action.Attack]:
        return self.actions.act_to_dir(direction)

    def wait(self) -> Literal[Action.Wait]:
        return self.actions.wait()

    def look(self) -> Literal[Action.No_Action]:
        coord = self.coord
        drawline_flag = False
        direction = Dir.Stay
        while True:
            new_coord = add_vector(coord, direction)
            if self.actions.level.is_legal(new_coord):
                coord = new_coord
            self.io.msg(self.actions.level.look_information(coord))
            if drawline_flag:
                self.io.draw_line(self.coord, coord, ("*", ColorPairs.Yellow))
                self.io.draw_line(coord, self.coord, ("*", ColorPairs.Yellow))
                self.io.msg(f"LoS: {self.actions.level.check_los(self.coord, coord)}")
            if coord != self.coord:
                symbol, (foreground, background) = self.actions.level.visible_char(coord)
                char = symbol, (foreground, Color.Green)
                self.io.draw_char(char, coord)
                self.io.draw_char(self.actions.level.visible_char(self.coord), self.coord, reverse=True)
            key = self.io.get_key()
            self.actions.redraw_no_action()
            direction = Dir.Stay
            if key in Binds.Directions:
                direction = Binds.get_direction(key)
            elif key == 'd':
                drawline_flag = not drawline_flag
            elif key == 'b':
                from pyrl.functions.coord_algorithms import bresenham
                for coord in bresenham(self.coord, coord):
                    self.io.msg(coord)
            elif key == 's':
                if coord in self.actions.level.creatures:
                    from pyrl.user_interface.status_texts import register_status_texts
                    register_status_texts(self.io, self.actions.game, self.actions.level.creatures[coord])
            elif key in Binds.Cancel or key in Binds.Look_Mode:
                break
        return Action.No_Action

    def quit(self, dont_ask: bool = True) -> Literal[Action.No_Action]:
        query = f"Do you wish to end the game? [{Binds.Strong_Yes}]"
        if dont_ask or self.io.get_key(query) in Binds.Strong_Yes:
            self.actions.quit()
        return Action.No_Action

    def save(self, dont_ask: bool = True) -> Literal[Action.Save, Action.No_Action]:
        query = f"Do you wish to save the game? [{Binds.Yes}]"
        if dont_ask or self.io.get_key(query) in Binds.Yes:
            self.io.msg("Saving...")
            return self.actions.save()
        return Action.No_Action

    def attack(self) -> Literal[Action.Attack, Action.No_Action]:
        query = f"Specify attack direction, {Binds.Cancel.key} to abort"
        key = self.io.get_key(query, keys=Binds.Directions + Binds.Cancel)
        if key in Binds.Directions:
            return self.actions.attack(Binds.get_direction(key))
        return Action.No_Action

    def redraw(self) -> Literal[Action.Redraw]:
        return self.actions.redraw()

    def descend(self) -> Literal[Action.Enter_Passage, Action.Teleport]:
        location = self.actions.get_passage()
        # Implicitly every non-up passage is a down-passage
        if location and location != DefaultLocation.Passage_Up:
            return self.actions.enter_passage()
        else:
            return self.debug_action.teleport_to_location(DefaultLocation.Passage_Down)
            # raise NoValidTargetException("You don't find any downwards passage.")

    def ascend(self) -> Literal[Action.Enter_Passage, Action.Teleport]:
        location = self.actions.get_passage()
        if location == DefaultLocation.Passage_Up:
            return self.actions.enter_passage()
        else:
            return self.debug_action.teleport_to_location(DefaultLocation.Passage_Up)
            # raise NoValidTargetException("You don't find any upwards passage.")

    def show_vision(self) -> Literal[Action.Redraw]:
        Config.clearly_show_vision = not Config.clearly_show_vision
        return self.actions.redraw()

    def print_history(self) -> Literal[Action.No_Action]:
        header = "History"
        lines_view(self.io.whole_window, build_lines(reversed(self.io.message_bar.history)), header=header)
        return Action.No_Action

    def manage_equipment(self) -> Literal[Action.No_Action, Action.Drop_Items]:
        return equipment_view(self.actions)

    def manage_backpack(self) -> Literal[Action.Drop_Items, Action.No_Action]:
        return backpack_view(self.actions)

    def pickup_items(self) -> Literal[Action.Pick_Items, Action.No_Action]:
        return pickup_items_view(self.actions)

    def drop_items(self) -> Literal[Action.Drop_Items, Action.No_Action]:
        return drop_items_view(self.actions)

    def init_walk_mode(self, instant_direction: Direction | None = None) -> Literal[Action.Move, Action.No_Action]:
        return self.walk_mode.init_walk_mode(instant_direction)

    def help_screen(self) -> Literal[Action.Redraw]:
        help_view(self.io)
        return self.actions.redraw()

    def toggle_fullscreen(self) -> Literal[Action.No_Action]:
        self.io.wrapper.toggle_fullscreen()
        return Action.No_Action

    def next_tileset(self) -> Literal[Action.Redraw]:
        tileset_name = self.io.wrapper.next_tileset()
        logging.debug(tileset_name)
        self.io.msg(tileset_name)
        return self.actions.redraw()

    def previous_tileset(self) -> Literal[Action.Redraw]:
        tileset_name = self.io.wrapper.previous_tileset()
        logging.debug(tileset_name)
        self.io.msg(tileset_name)
        return self.actions.redraw()

    def next_bdf(self) -> Literal[Action.Redraw]:
        tileset_name = self.io.wrapper.next_bdf()
        # logging.debug(tileset_name)
        self.io.msg(tileset_name)
        return self.actions.redraw()

    def previous_bdf(self) -> Literal[Action.Redraw]:
        tileset_name = self.io.wrapper.previous_bdf()
        # logging.debug(tileset_name)
        self.io.msg(tileset_name)
        return self.actions.redraw()
