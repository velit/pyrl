"""pyrl; Python roguelike by Veli Tapani Kiiskinen."""
from __future__ import annotations

import sys
from typing import NoReturn, Any

from pyrl import state_store
from pyrl.algorithms.field_of_vision import ShadowCast
from pyrl.config.binds import Binds
from pyrl.config.config import Config
from pyrl.config.debug import Debug
from pyrl.controllers.ai_controller import AIController, AiState
from pyrl.controllers.user_controller import UserController
from pyrl.creature.action import Action
from pyrl.creature.creature import Creature
from pyrl.creature.mixins.visionary import Visionary
from pyrl.creature.player import Player
from pyrl.creature.creature_actions import CreatureActions
from pyrl.game_data.pyrl_world import pyrl_world
from pyrl.io_wrappers.io_wrapper import IoWrapper
from pyrl.structures.helper_mixins import HasCreatureActions
from pyrl.types.world_point import WorldPoint
from pyrl.user_interface.status_texts import register_status_texts
from pyrl.window.window_system import WindowSystem
from pyrl.world.level import Level

class Game:

    def __init__(self, game_name: str, cursor_lib: IoWrapper) -> None:
        self.game_name = game_name
        self.ai_state: AiState = {}
        self.turn_counter = 0
        self.time = 0

        self.world = pyrl_world()
        self.io, \
            self.creature_actions, \
            self.ai_controller, \
            self.user_controller = self.post_init(cursor_lib)

    def post_init(self, cursor_lib: IoWrapper) -> tuple[WindowSystem, CreatureActions, AIController, UserController]:
        """Initialise non-serialized state. Used when loading the game."""
        self.io = WindowSystem(cursor_lib)
        self.creature_actions = CreatureActions(self)
        self.ai_controller = AIController(self.ai_state, self.creature_actions)
        self.user_controller = UserController(self.creature_actions)
        register_status_texts(self.io, self, self.player)
        return self.io, self.creature_actions, self.ai_controller, self.user_controller

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

        while True:
            creature, time_delta = self.active_level.turn_scheduler.advance_time()
            self.time += time_delta

            self.creature_actions.associate_creature(creature)
            if creature is self.player:
                assert isinstance(creature, Visionary)
                self.update_view(creature)
                action_cost = self.player_act()
                if action_cost > 0:
                    self.turn_counter += 1
            else:
                action_cost = self.ai_act()

            creature_check, time_delta = self.active_level.turn_scheduler.addpop(creature, action_cost)
            assert creature is creature_check
            assert time_delta == 0

    def player_act(self) -> int:
        """Returns the action cost"""
        while (action := self.user_controller.act()) == Action.No_Action:
            pass
        return self.creature_actions.verify_and_get_cost(action)

    def ai_act(self) -> int:
        """Returns the action cost"""
        action = self.ai_controller.act(self.player.coord)
        assert action != Action.No_Action, "AI chose {action=}"
        return self.creature_actions.verify_and_get_cost(action)

    def move_creature_to_level(self, creature: Creature, world_point: WorldPoint) -> bool:
        try:
            target_level = self.world.get_level(world_point.level_key)
        except KeyError:
            return False

        target_level.move_creature_to_location(creature, world_point.level_location)

        if isinstance(creature, Visionary):
            creature.vision.clear()

        if creature is self.player:
            self.redraw()

        return True

    def creature_death(self, creature: Creature) -> None:
        self.ai_controller.remove_creature_state(creature)
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

    def update_view(self, creature: Visionary) -> None:
        """
        Update the vision set of the Visionary.
        """
        lvl = creature.level
        new_vision = ShadowCast.get_light_set(lvl.is_see_through, creature.coord, creature.sight, lvl.rows, lvl.cols)
        creature.vision, old_vision = new_vision, creature.vision
        potentially_modified_vision = new_vision | old_vision

        if Debug.show_map:
            vision_info = lvl.get_vision_information(lvl.tiles.coord_iter(), new_vision, always_show_creatures=True)
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
            vision_info = lvl.get_vision_information(draw_coords, self.player.vision, always_show_creatures=True)
        else:
            draw_coords = self.player.get_visited_locations() | self.player.vision
            vision_info = lvl.get_vision_information(draw_coords, self.player.vision)
        self.io.draw(vision_info)

        if Config.clearly_show_vision:
            reverse_data = lvl.get_vision_information(self.player.vision, self.player.vision)
            self.io.draw(reverse_data, True)

    def __getstate__(self) -> dict[str, Any]:
        exclude_state = (
            'ai_controller',
            'creature_actions'
            'io',
            'user_controller',
        )
        state = vars(self).copy()
        for item in exclude_state:
            del state[item]
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        vars(self).update(state)
