from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial

from pyrl.config.binds import Binds
from pyrl.config.config import Config
from pyrl.controllers.user.debug_action import DebugAction
from pyrl.controllers.user.messages.combat import combat_message, experience_message
from pyrl.controllers.user.messages.generic import article
from pyrl.controllers.user.messages.items import item_description
from pyrl.controllers.user.walk_mode import WalkMode
from pyrl.engine.actions.action import Action
from pyrl.engine.actions.action_exceptions import ActionException
from pyrl.engine.actions.action_feedback import ActionFeedback, NoActionFeedback, AttackFeedback, DropItemsFeedback, \
    PickItemsFeedback, DisplacementFeedback
from pyrl.engine.actions.action_interface import ActionInterface
from pyrl.functions.coord_algorithms import add_vector
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.structures.helper_mixins import CreatureActionsMixin
from pyrl.types.glyphs import Color, Colors
from pyrl.types.directions import Direction, Dir
from pyrl.types.keys import Key, KeyTuple, AnyKey
from pyrl.user_interface.help_view import help_view
from pyrl.user_interface.inventory_views import equipment_view, backpack_view, pickup_items_view, drop_items_view
from pyrl.user_interface.lines_view import lines_view, build_color_lines

ActionCallable = Callable[[], ActionFeedback]
ActionLookup = dict[AnyKey, ActionCallable]

@dataclass
class UserController(CreatureActionsMixin):
    actions: ActionInterface

    walk_mode:     WalkMode     = field(init=False)
    debug_action:  DebugAction  = field(init=False)
    action_lookup: ActionLookup = field(init=False)

    def __post_init__(self) -> None:
        self.walk_mode = WalkMode(self.actions)
        self.debug_action = DebugAction(self.actions)
        self.action_lookup = self.define_actions()

    def define_actions(self) -> dict[str, ActionCallable]:
        action_lookup: ActionLookup = {
            '+':               partial(self.debug_action.sight_change, 1),
            '-':               partial(self.debug_action.sight_change, -1),
            Key.WINDOW_RESIZE: self.redraw,
            Key.CLOSE_WINDOW:  self.quit,
        }

        unfinalized_actions: dict[KeyTuple, ActionCallable] = {
            Binds.Debug_Commands:    self.debug_action.ask_action,
            Binds.Quit:              self.quit,
            Binds.Save:              self.save,
            Binds.Attack:            self.attack,
            Binds.Redraw:            self.redraw,
            Binds.History:           self.print_history,
            Binds.Look_Mode:         self.look,
            Binds.Help:              self.help_screen,
            Binds.Equipment:         self.manage_equipment,
            Binds.Backpack:          self.manage_backpack,
            Binds.Pick_Up_Items:     self.pickup_items,
            Binds.Drop_Items:        self.drop_items,
            Binds.Walk_Mode:         self.init_walk_mode,
            Binds.Show_Vision:       self.show_vision,
            Binds.Ascend:            self.ascend,
            Binds.Descend:           self.descend,
            Binds.Toggle_Fullscreen: self.toggle_fullscreen,
            Binds.Next_Tileset:      self.next_tileset,
            Binds.Previous_Tileset:  self.previous_tileset,
            Binds.Next_Bdf:          self.next_bdf,
            Binds.Previous_Bdf:      self.previous_bdf,

            Binds.North:             partial(self.act_to_dir, Dir.North),
            Binds.NorthEast:         partial(self.act_to_dir, Dir.NorthEast),
            Binds.East:              partial(self.act_to_dir, Dir.East),
            Binds.SouthEast:         partial(self.act_to_dir, Dir.SouthEast),
            Binds.South:             partial(self.act_to_dir, Dir.South),
            Binds.SouthWest:         partial(self.act_to_dir, Dir.SouthWest),
            Binds.West:              partial(self.act_to_dir, Dir.West),
            Binds.NorthWest:         partial(self.act_to_dir, Dir.NorthWest),
            Binds.Stay:              self.wait,

            Binds.Instant_North:     partial(self.init_walk_mode, Dir.North),
            Binds.Instant_NorthEast: partial(self.init_walk_mode, Dir.NorthEast),
            Binds.Instant_East:      partial(self.init_walk_mode, Dir.East),
            Binds.Instant_SouthEast: partial(self.init_walk_mode, Dir.SouthEast),
            Binds.Instant_South:     partial(self.init_walk_mode, Dir.South),
            Binds.Instant_SouthWest: partial(self.init_walk_mode, Dir.SouthWest),
            Binds.Instant_West:      partial(self.init_walk_mode, Dir.West),
            Binds.Instant_NorthWest: partial(self.init_walk_mode, Dir.NorthWest),
            Binds.Instant_Stay:      partial(self.init_walk_mode, Dir.Stay),
        }

        for keys, action_func in unfinalized_actions.items():
            for key in keys:
                action_lookup[key] = action_func

        return action_lookup

    def act(self) -> Action:
        try:
            feedback = self._get_and_execute_action()
        except ActionException as exception:
            self.io.msg(exception.player_message)
            feedback = NoActionFeedback

        self.process_feedback(feedback)
        return feedback.action

    def process_feedback(self, feedback: ActionFeedback) -> None:
        match feedback:

            case DisplacementFeedback(action, coord, items):
                if self.actions.get_passage():
                    self.io.msg(f"There is {article(self.actions.get_tile().name)} here.")
                if items:
                    self.io.msg(f"There {item_description(items, use_verb=True)} here.")

            case DropItemsFeedback(items):
                self.io.msg(f"Dropped {item_description(items)}")

            case PickItemsFeedback(items):
                self.io.msg(f"Picked up {item_description(items)}")

            case AttackFeedback(attacker, target, succeeds, target_died, damage, experience, levelups):
                combat_msg = combat_message(attacker, target, self.player, succeeds, target_died, damage)
                color = Colors.Normal
                if target is self.player and damage:
                    if damage / self.player.max_hp >= 0.25 or self.player.hp / self.player.max_hp < 0.3:
                        color = Colors.Red
                    else:
                        color = Colors.Light_Red
                self.io.msg(combat_msg, color=color)
                if target is self.player and target_died:
                    self.io.msg("You", color=Colors.Dark)
                    self.io.msg("die...", color=Colors.Darker)
                    self.io.get_key(keys=Binds.Cancel)
                if experience:
                    self.io.msg(f"{experience_message(experience)} xp.", color=Colors.Green)
                if levelups:
                    self.io.msg(f"Congratulations! you've gained enough experience to attain level {levelups[-1]}!",
                                color=Colors.Yellow)

    def _get_and_execute_action(self) -> ActionFeedback:
        if self.walk_mode.active:
            return self.walk_mode.continue_walk()
        key = self.io.get_key()
        if key in self.action_lookup:
            return self.action_lookup[key]()
        else:
            self.io.msg(f"Undefined key: {key}")
            return NoActionFeedback

    def act_to_dir(self, direction: Direction) -> ActionFeedback:
        return self.actions.act_to_dir(direction)

    def wait(self) -> ActionFeedback:
        return self.actions.wait()

    def look(self) -> ActionFeedback:
        coord = self.coord
        drawline_flag = False
        direction = Dir.Stay
        while True:
            new_coord = add_vector(coord, direction)
            if self.actions.level.is_legal(new_coord):
                coord = new_coord
            self.io.msg(self.actions.level.look_information(coord))
            if drawline_flag:
                self.io.draw_line(self.coord, coord, ("*", Colors.Yellow))
                self.io.draw_line(coord, self.coord, ("*", Colors.Yellow))
                self.io.msg(f"LoS: {self.actions.level.check_los(self.coord, coord)}")
            if coord != self.coord:
                symbol, (foreground, background) = self.actions.level.visible_glyph(coord)
                glyph = symbol, (foreground, Color.Green)
                self.io.draw_glyph(glyph, coord)
                self.io.draw_glyph(self.actions.level.visible_glyph(self.coord), self.coord, reverse=True)
            key = self.io.get_key()
            self.actions.redraw()
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
        return NoActionFeedback

    def quit(self, dont_ask: bool = True) -> ActionFeedback:
        query = f"Do you wish to end the game? [{Binds.Strong_Yes}]"
        if dont_ask or self.io.get_key(query) in Binds.Strong_Yes:
            self.actions.quit()
        return NoActionFeedback

    def save(self, dont_ask: bool = True) -> ActionFeedback:
        query = f"Do you wish to save the game? [{Binds.Yes}]"
        if dont_ask or self.io.get_key(query) in Binds.Yes:
            self.io.msg("Saving...")
            return self.actions.save()
        return NoActionFeedback

    def attack(self) -> ActionFeedback:
        query = f"Specify attack direction, {Binds.Cancel.key} to abort"
        key = self.io.get_key(query, keys=Binds.Directions + Binds.Cancel)
        if key in Binds.Directions:
            return self.actions.attack(Binds.get_direction(key))
        return NoActionFeedback

    def redraw(self) -> ActionFeedback:
        return self.actions.redraw_action()

    def descend(self) -> ActionFeedback:
        location = self.actions.get_passage()
        # Implicitly every non-up passage is a down-passage
        if location and location != DefaultLocation.Passage_Up:
            return self.actions.enter_passage()
        else:
            return self.debug_action.teleport_to_location(DefaultLocation.Passage_Down)
            # raise NoValidTargetException("You don't find any downwards passage.")

    def ascend(self) -> ActionFeedback:
        location = self.actions.get_passage()
        if location == DefaultLocation.Passage_Up:
            return self.actions.enter_passage()
        else:
            return self.debug_action.teleport_to_location(DefaultLocation.Passage_Up)
            # raise NoValidTargetException("You don't find any upwards passage.")

    def show_vision(self) -> ActionFeedback:
        Config.clearly_show_vision = not Config.clearly_show_vision
        return self.actions.redraw_action()

    def print_history(self) -> ActionFeedback:
        header = "History"
        lines_view(self.io.whole_window, build_color_lines(reversed(self.io.message_bar.history)), header=header)
        return NoActionFeedback

    def manage_equipment(self) -> ActionFeedback:
        return equipment_view(self.actions)

    def manage_backpack(self) -> ActionFeedback:
        return backpack_view(self.actions)

    def pickup_items(self) -> ActionFeedback:
        return pickup_items_view(self.actions)

    def drop_items(self) -> ActionFeedback:
        return drop_items_view(self.actions)

    def init_walk_mode(self, instant_direction: Direction | None = None) -> ActionFeedback:
        return self.walk_mode.init_walk_mode(instant_direction)

    def help_screen(self) -> ActionFeedback:
        help_view(self.io)
        return self.actions.redraw_action()

    def toggle_fullscreen(self) -> ActionFeedback:
        self.io.wrapper.toggle_fullscreen()
        return NoActionFeedback

    def next_tileset(self) -> ActionFeedback:
        tileset_name = self.io.wrapper.next_tileset()
        logging.debug(tileset_name)
        self.io.msg(tileset_name)
        return self.actions.redraw_action()

    def previous_tileset(self) -> ActionFeedback:
        tileset_name = self.io.wrapper.previous_tileset()
        logging.debug(tileset_name)
        self.io.msg(tileset_name)
        return self.actions.redraw_action()

    def next_bdf(self) -> ActionFeedback:
        tileset_name = self.io.wrapper.next_bdf()
        # logging.debug(tileset_name)
        self.io.msg(tileset_name)
        return self.actions.redraw_action()

    def previous_bdf(self) -> ActionFeedback:
        tileset_name = self.io.wrapper.previous_bdf()
        # logging.debug(tileset_name)
        self.io.msg(tileset_name)
        return self.actions.redraw_action()
