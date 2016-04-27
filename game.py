"""pyrl; Python roguelike by Veli Tapani Kiiskinen."""
from __future__ import absolute_import, division, print_function, unicode_literals

import state_store
from game_data.pyrl_world import get_world
from ai import AI
from config.debug import Debug
from config.game import GameConf
from bindings import Bind
from fov import ShadowCast
from game_actions import GameActions
from interface.status_texts import register_status_texts
from controllers.user_controller import UserController
from window.window_system import WindowSystem
from world.world import LevelNotFound


class Game(object):

    def __init__(self, game_name, cursor_lib):
        self.game_name = game_name
        self.ai = AI()
        self.turn_counter = 0
        self.time = 0

        self.world = get_world()
        self.io, self.user_controller = self.init_nonserializable_objects(cursor_lib)

    def init_nonserializable_objects(self, cursor_lib_callback):
        self.io = WindowSystem(cursor_lib_callback())
        self.user_controller = UserController(GameActions(self, self.player))
        register_status_texts(self.io, self, self.player)
        return self.io, self.user_controller

    player = property(lambda self: self.world.player)
    active_level = property(lambda self: self.world.player.level)

    def main_loop(self):
        ai_game_actions = GameActions(self)
        self.io.msg("{0} for help menu".format(Bind.Help.key))
        while True:
            creature, time_delta = self.active_level.turn_scheduler.advance_time()
            self.time += time_delta

            if creature is self.player:
                self.update_view(creature)
                self.user_controller.actions._clear_action()
                self.user_controller.act()
                action_cost = self.user_controller.actions.action_cost

                if action_cost > 0:
                    self.turn_counter += 1
            else:
                ai_game_actions._clear_action(and_associate_creature=creature)
                self.ai.act(ai_game_actions, self.player.coord)
                action_cost = ai_game_actions.action_cost

            assert action_cost >= 0, \
                "Negative cost actions are not allowed (yet at least).{}".format(action_cost)

            creature_check, time_delta = self.active_level.turn_scheduler.addpop(creature, action_cost)
            assert creature is creature_check
            assert time_delta == 0

    def move_creature_to_level(self, creature, world_point):
        try:
            target_level = self.world.get_level(world_point.level_key)
        except LevelNotFound:
            return False

        creature.level.remove_creature(creature)
        target_level.add_creature_to_location(creature, world_point.level_location)

        try:
            creature.vision.clear()
        except AttributeError:
            pass

        if creature is self.player:
            self.redraw()

        return True

    def creature_death(self, creature):
        self.ai.remove_creature_state(creature)
        if creature is self.player:
            self.io.notify("You die...")
            self.endgame(ask=False)
        creature.level.remove_creature(creature)

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

    def update_view(self, creature):
        """
        Update the vision set of the creature.

        This operation should only be done on creatures that have the .vision
        attribute ie. AdvancedCreatures for instance.
        """
        lvl = creature.level
        new_vision = ShadowCast.get_light_set(lvl.is_see_through, creature.coord,
                                              creature.sight, lvl.rows, lvl.cols)
        creature.vision, old_vision = new_vision, creature.vision

        creature_changed_vision = (new_vision ^ old_vision)
        creature_unchanged_vision = (new_vision & old_vision)
        level_changed_vision = creature.pop_modified_locations()

        if Debug.show_map:
            update_coords = creature_changed_vision | level_changed_vision
            vision_info = lvl.get_vision_information(update_coords, new_vision,
                                                       always_show_creatures=True)
        else:
            # new ^ old is the set of new squares in view and squares that were left # behind.
            # new & old & modified is the set of old squares still in view which had changes
            # since last turn.
            update_coords = creature_changed_vision | (creature_unchanged_vision & level_changed_vision)
            vision_info = lvl.get_vision_information(update_coords, new_vision)

        self.io.draw(vision_info)

        if GameConf.clearly_show_vision:
            reverse_data = lvl.get_vision_information(new_vision, new_vision)
            self.io.draw(reverse_data, True)

    def redraw(self):
        self.io.level_window.clear()
        lvl = self.active_level

        if Debug.show_map:
            draw_coords = lvl.tiles.coord_iter()
            vision_info = lvl.get_vision_information(draw_coords, self.player.vision,
                                                     always_show_creatures=True)
        else:
            draw_coords = self.player.get_visited_locations() | self.player.vision
            vision_info = lvl.get_vision_information(draw_coords, self.player.vision)
        self.io.draw(vision_info)

        if GameConf.clearly_show_vision:
            reverse_data = lvl.get_vision_information(self.player.vision, self.player.vision)
            self.io.draw(reverse_data, True)

    def __getstate__(self):
        exclude_state = ('user_controller', 'io')
        state = vars(self).copy()
        for item in exclude_state:
            del state[item]
        return state

    def __setstate__(self, state):
        vars(self).update(state)
