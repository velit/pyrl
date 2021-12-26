"""pyrl; Python roguelike by Veli Tapani Kiiskinen."""
from __future__ import annotations

import sys
from typing import NoReturn, Any

from pyrl import state_store
from pyrl.algorithms.field_of_vision import ShadowCast
from pyrl.config.binds import Binds
from pyrl.config.config import Config
from pyrl.config.debug import Debug
from pyrl.controllers.ai import AI
from pyrl.controllers.user_controller import UserController
from pyrl.creature.creature import Creature
from pyrl.creature.mixins.visionary import Visionary
from pyrl.creature.player import Player
from pyrl.game_actions import GameActions
from pyrl.game_data.pyrl_world import pyrl_world
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.types.world_point import WorldPoint
from pyrl.user_interface.status_texts import register_status_texts
from pyrl.window.window_system import WindowSystem
from pyrl.world.level import Level

class Game:

    def __init__(self, game_name: str, cursor_lib: IoWrapper) -> None:
        self.game_name = game_name
        self.ai = AI()
        self.turn_counter = 0
        self.time = 0

        self.world = pyrl_world()
        self.io, self.user_controller = self.init_nonserialized_state(cursor_lib)

    def init_nonserialized_state(self, cursor_lib: IoWrapper) -> tuple[WindowSystem, UserController]:
        self.io = WindowSystem(cursor_lib)
        self.user_controller = UserController(GameActions(self, self.player))
        register_status_texts(self.io, self, self.player)
        return self.io, self.user_controller

    @property
    def player(self) -> Player:
        return self.world.player

    @property
    def active_level(self) -> Level:
        return self.world.player.level

    def game_loop(self) -> NoReturn:
        self.io.msg(f"{Binds.Help.key} for help menu.")
        undefined_keys = Binds.undefined_keys()
        if undefined_keys:
            self.io.msg(f"Following actions are missing from bind config: {', '.join(undefined_keys)}")

        ai_game_actions = GameActions(self)
        while True:
            creature, time_delta = self.active_level.turn_scheduler.advance_time()
            self.time += time_delta

            if creature is self.player:
                self.update_view(creature)
                self.user_controller.actions._clear_action()
                self.user_controller.act()
                action_cost = self.user_controller.actions.action_cost
                assert action_cost is not None, "Player returned control without setting action cost"
                if action_cost > 0:
                    self.turn_counter += 1
            else:
                ai_game_actions._clear_action(and_associate_creature=creature)
                self.ai.act(ai_game_actions, self.player.coord)
                action_cost = ai_game_actions.action_cost

            assert action_cost is not None, "Creature returned control without setting action cost"
            assert action_cost >= 0, \
                f"Negative {action_cost=} are not allowed (yet at least)."

            creature_check, time_delta = self.active_level.turn_scheduler.addpop(creature, action_cost)
            assert creature is creature_check
            assert time_delta == 0

    def move_creature_to_level(self, creature: Creature, world_point: WorldPoint) -> bool:
        try:
            target_level = self.world.get_level(world_point.level_key)
        except KeyError:
            return False

        creature.level.remove_creature(creature)
        target_level.add_creature_to_location(creature, world_point.level_location)

        if isinstance(creature, Visionary):
            creature.vision.clear()

        if creature is self.player:
            self.redraw()

        return True

    def creature_death(self, creature: Creature) -> None:
        self.ai.remove_creature_state(creature)
        if creature is self.player:
            self.io.get_key("You die...", keys=Binds.Cancel)
            self.endgame()
        creature.level.remove_creature(creature)

    def endgame(self) -> NoReturn:
        sys.exit(0)

    def savegame(self) -> str:
        try:
            raw, compressed = state_store.save(self, self.game_name)
        except IOError as e:
            msg_str = str(e)
        else:
            msg_str = f"Saved game '{self.game_name}', file size: {raw:,} b," \
                      f" {compressed:,} b compressed. Ratio: {raw / compressed:.2%}"
        return msg_str

    def update_view(self, creature: Creature) -> None:
        """
        Update the vision set of the creature.

        This operation should only be done on creatures that have the .vision
        attribute i.e. Player for instance.
        """
        if not isinstance(creature, Visionary):
            raise ValueError("Creature {} doesn't have the capacity to remember its vision.")
        if not isinstance(creature, Creature):
            raise ValueError(f"{creature} is not a creature!")

        lvl = creature.level
        new_vision = ShadowCast.get_light_set(lvl.is_see_through, creature.coord, creature.sight, lvl.rows, lvl.cols)
        creature.vision, old_vision = new_vision, creature.vision
        potentially_modified_vision = new_vision | old_vision

        if Debug.show_map:
            vision_info = lvl.get_vision_information(lvl.tiles.coord_iter(), new_vision,
                                                     always_show_creatures=True)
        else:
            vision_info = lvl.get_vision_information(potentially_modified_vision, new_vision)

        self.io.draw(vision_info)

        if Config.clearly_show_vision:
            reverse_data = lvl.get_vision_information(new_vision, new_vision)
            self.io.draw(reverse_data, True)

    def redraw(self) -> None:
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

        if Config.clearly_show_vision:
            reverse_data = lvl.get_vision_information(self.player.vision, self.player.vision)
            self.io.draw(reverse_data, True)

    def __getstate__(self) -> dict[str, Any]:
        exclude_state = ('user_controller', 'io')
        state = vars(self).copy()
        for item in exclude_state:
            del state[item]
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        vars(self).update(state)
