"""pyrl; Python roguelike by Tapani Kiiskinen."""
from __future__ import absolute_import, division, print_function, unicode_literals

import state_store
from game_data.pyrl_world import get_world
from ai import AI
from config.debug import Debug
from config.game import GameConf
from config.bindings import Bind
from fov import ShadowCast
from game_actions import GameActions
from interface.status_texts import register_status_texts
from user_controller import UserController
from window.window_system import WindowSystem
from world import LevelNotFound


class Game(object):

    def __init__(self, game_name, cursor_lib):
        self.game_name = game_name
        self.turn_counter = 0
        self.ai = AI()
        self.time = 0
        self.modified_locations = set()
        self.vision_cache = None
        self.save_mark = False

        self.world = get_world()
        self.player = self.world.player
        self.world.get_level(self.world.start_level, self.add_modified_location)

        self.init_nonserial_objects(cursor_lib, self.player)

    def init_nonserial_objects(self, cursor_lib_callback, player):
        self.io = WindowSystem(cursor_lib_callback())
        self.user_input = UserController(GameActions(self, player), self.io)
        register_status_texts(self, player)

    def main_loop(self):
        ai_game_actions = GameActions(self)
        self.io.msg("{0} for help menu".format(Bind.Help.key))
        while True:
            if self.save_mark:
                self.savegame(ask=False)
                self.save_mark = False

            creature, time_delta = self.player.level.turn_scheduler.advance_time()
            self.time += time_delta

            if creature is self.player:
                self.update_view(creature)
                self.user_input.game_actions.clear_action()
                self.user_input.get_user_input_and_act()
                action_cost = self.user_input.game_actions.action_cost

                if action_cost > 0:
                    self.turn_counter += 1
            else:
                ai_game_actions.clear_action(and_associate_creature=creature)
                self.ai.act_alert(ai_game_actions, self.player.coord)
                action_cost = ai_game_actions.action_cost

            assert action_cost >= 0, "Negative cost actions are not allowed.  {}".format(action_cost)

            creature.level.turn_scheduler.add(creature, action_cost)

    def move_creature_to_level(self, creature, world_point):
        level_key, level_location = world_point
        try:
            target_level = self.world.get_level(level_key, self.add_modified_location)
        except LevelNotFound:
            return False

        creature.level.remove_creature(creature, turnscheduler_remove=False)
        target_level.add_creature_to_location(creature, level_location)

        try:
            creature.vision.clear()
        except AttributeError:
            pass

        if creature is self.player:
            self.pop_modified_locations()
            self.redraw()

        return True

    def creature_death(self, creature):
        self.ai.remove_creature_state(creature)
        level = creature.level
        if creature is self.player:
            self.io.notify("You die...")
            self.endgame(ask=False)
        level.remove_creature(creature, turnscheduler_remove=True)

    def endgame(self, ask=True):
        if not ask or self.io.ask("Do you wish to end the game? [y/N]") in GameConf.YES:
            exit()

    def savegame(self, ask=True):
        if not ask or self.io.ask("Do you wish to save the game? [y/N]") in GameConf.YES:
            self.io.msg("Saving...")
            self.io.refresh()

            try:
                raw, compressed = state_store.save(self, self.game_name)
            except IOError as e:
                msg_str = str(e)
            else:
                msg_str = "Saved game '{}', file size: {:,} b, {:,} b compressed. Ratio: {:.2%}"
                msg_str = msg_str.format(self.game_name, raw, compressed, raw / compressed)
            self.io.msg(msg_str)

    def add_modified_location(self, coord):
        self.modified_locations.add(coord)

    def pop_modified_locations(self):
        locations = self.modified_locations
        self.modified_locations = set()
        return locations

    def update_view(self, creature):
        """
        Update the vision set of the creature.

        This operation should only be done on creatures that have the .vision
        attribute ie. AdvancedCreatures for instance.
        """
        level = creature.level
        new_vision = ShadowCast.get_light_set(level.is_see_through, creature.coord,
                                              creature.sight, level.rows, level.cols)

        modified = self.pop_modified_locations()
        creature.vision, old_vision = new_vision, creature.vision

        if not Debug.show_map:
            # new ^ old is the set of new squares in view and squares that were left # behind.
            # new & old & modified is the set of squares still in view which had changes
            # since last turn.
            update_set = (new_vision ^ old_vision) | (new_vision & old_vision & modified)
            updated_vision_data = level.get_vision_information(update_set, new_vision)
        else:
            update_set = (new_vision ^ old_vision) | modified
            updated_vision_data = level.get_vision_information(update_set, new_vision, always_show_creatures=True)

        self.io.draw(updated_vision_data)

        if Debug.reverse:
            reverse_data = level.get_vision_information(new_vision, new_vision)
            self.io.draw(reverse_data, Debug.reverse)

    def redraw(self):
        self.io.level_window.clear()
        level = self.player.level

        if not Debug.show_map:
            draw_set = self.player.get_visited_locations() | self.player.vision
            draw_data = level.get_vision_information(draw_set, self.player.vision)
        else:
            draw_set = level.get_coord_iter()
            draw_data = level.get_vision_information(draw_set, self.player.vision,
                                                     always_show_creatures=True)
        self.io.draw(draw_data)

        if Debug.reverse:
            reverse_data = level.get_vision_information(self.player.vision,
                                                        self.player.vision)
            self.io.draw(reverse_data, Debug.reverse)

    def __getstate__(self):
        exclude_state = ('user_input', 'io')
        state = vars(self).copy()
        for item in exclude_state:
            del state[item]
        return state

    def __setstate__(self, state):
        vars(self).update(state)
