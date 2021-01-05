"""pyrl; Python roguelike by Veli Tapani Kiiskinen."""
from pyrl import state_store, binds
from pyrl.ai import AI
from pyrl.binds import Binds
from pyrl.config.debug import Debug
from pyrl.config.game import GameConf
from pyrl.controllers.user_controller import UserController
from pyrl.fov import ShadowCast
from pyrl.game_actions import GameActions
from pyrl.game_data.pyrl_world import get_world
from pyrl.interface.status_texts import register_status_texts
from pyrl.window.window_system import WindowSystem
from pyrl.world.world import LevelNotFound
from pyrl.creature.remembers_vision import RemembersVision


class Game(object):

    def __init__(self, game_name, cursor_lib):
        self.game_name = game_name
        self.ai = AI()
        self.turn_counter = 0
        self.time = 0

        self.world = get_world()
        self.io, self.user_controller = self.init_nonserialized_state(cursor_lib)

    def init_nonserialized_state(self, cursor_lib):
        self.io = WindowSystem(cursor_lib)
        self.user_controller = UserController(GameActions(self, self.player))
        register_status_texts(self.io, self, self.player)
        return self.io, self.user_controller

    player = property(lambda self: self.world.player)
    active_level = property(lambda self: self.world.player.level)

    def game_loop(self):
        ai_game_actions = GameActions(self)
        self.io.msg("{0} for help menu.".format(Binds.Help.key))
        undefined_keys = binds.undefined_keys()
        if undefined_keys:
            self.io.msg(f"Following actions are missing from bind config: {', '.join(undefined_keys)}")
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
            self.io.get_key("You die...", keys=Binds.Cancel)
            self.endgame()
        creature.level.remove_creature(creature)

    def endgame(self):
        exit()

    def savegame(self):
        try:
            raw, compressed = state_store.save(self, self.game_name)
        except IOError as e:
            msg_str = str(e)
        else:
            msg_str = "Saved game '{}', file size: {:,} b, {:,} b compressed. Ratio: {:.2%}"
            msg_str = msg_str.format(self.game_name, raw, compressed, raw / compressed)
        return msg_str

    def update_view(self, creature):
        """
        Update the vision set of the creature.

        This operation should only be done on creatures that have the .vision
        attribute ie. AdvancedCreatures for instance.
        """
        if not isinstance(creature, RemembersVision):
            raise ValueError("Creature {} doesn't have the capacity to remember its vision.")

        lvl = creature.level
        new_vision = ShadowCast.get_light_set(lvl.is_see_through, creature.coord,
                                              creature.sight, lvl.rows, lvl.cols)
        creature.vision, old_vision = new_vision, creature.vision
        potentially_modified_vision = new_vision | old_vision

        if Debug.show_map:
            vision_info = lvl.get_vision_information(lvl.tiles.coord_iter(), new_vision,
                                                       always_show_creatures=True)
        else:
            vision_info = lvl.get_vision_information(potentially_modified_vision, new_vision)

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
