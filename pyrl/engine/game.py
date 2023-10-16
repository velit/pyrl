"""pyrl; Python roguelike by Veli Tapani Kiiskinen."""
from __future__ import annotations

import sys
from collections.abc import Sequence
from dataclasses import field, InitVar, dataclass
from typing import NoReturn, Any

from pyrl.config.binds import Binds
from pyrl.config.config import Config
from pyrl.config.debug import Debug
from pyrl.controllers.ai_controller import AIController, AiState
from pyrl.controllers.user.user_controller import UserController
from pyrl.engine import state_store
from pyrl.engine.actions.action import Action
from pyrl.engine.actions.action_feedback import AttackFeedback
from pyrl.engine.actions.action_interface import ActionInterface
from pyrl.engine.behaviour.combat import calc_melee_attack
from pyrl.engine.behaviour.field_of_vision import ShadowCast
from pyrl.engine.creature.advanced.mixins.visionary import Visionary
from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.advanced.player import Player
from pyrl.engine.creature.enums.stats import Stat
from pyrl.engine.enums.glyphs import Colors
from pyrl.engine.world.level import Level
from pyrl.engine.world.tile import Tile
from pyrl.engine.world.world import World
from pyrl.engine.world.enums.world_point import WorldPoint
from pyrl.game_data.pyrl_world import pyrl_world
from pyrl.ui.io_lib.protocol.io_wrapper import IoWrapper
from pyrl.ui.views.status_texts import register_status_texts
from pyrl.ui.window.window_system import WindowSystem


@dataclass
class Game:
    game_name:        str
    cursor_lib:       InitVar[IoWrapper] = field(repr=False)

    ai_state:         AiState            = field(init=False, repr=False, default_factory=dict)
    world:            World              = field(init=False, repr=False, default_factory=pyrl_world)

    io:               WindowSystem       = field(init=False, repr=False)
    action_interface: ActionInterface    = field(init=False, repr=False)
    ai_controller:    AIController       = field(init=False, repr=False)
    user_controller:  UserController     = field(init=False, repr=False)

    def __post_init__(self, cursor_lib: IoWrapper) -> None:
        """Initialize non-serialised state. Used when loading the game."""
        self.io = WindowSystem(cursor_lib)
        self.action_interface = ActionInterface(self)
        self.ai_controller = AIController(self.ai_state, self.action_interface)
        self.user_controller = UserController(self.action_interface)
        register_status_texts(self.io, self, self.player)

    @property
    def player(self) -> Player:
        return self.world.player

    @property
    def active_level(self) -> Level:
        return self.world.player.level

    def game_loop(self) -> NoReturn:
        self.io.msg(f"{Binds.Help.key} for help menu.", color=Colors.Yellow)
        undefined_keys = Binds.undefined_keys()
        if undefined_keys:
            self.io.msg(f"Following actions are missing from bind config: {', '.join(undefined_keys)}")

        while True:
            creature, ticks_delta = self.active_level.turn_scheduler.pop()
            self.world.ticks += ticks_delta
            cost = 0
            try:
                action, cost = self.creature_act(creature)
            finally:
                creature.level.turn_scheduler.add(creature, cost)

            if action == Action.Save:
                self.io.msg(self.save_game())

    def creature_act(self, creature: Creature) -> tuple[Action, int]:
        creature.advance_time(self.world.ticks)
        self.action_interface.associate_creature(creature)
        if creature is self.player:
            assert isinstance(creature, Visionary)
            self.update_view(creature)
            return self.get_player_action()
        else:
            return self.get_ai_action()

    def get_player_action(self) -> tuple[Action, int]:
        """Returns the action cost"""
        while (action := self.user_controller.act()) == Action.No_Action:
            pass
        return action, self.action_interface.verify_and_get_cost(action)

    def get_ai_action(self) -> tuple[Action, int]:
        """Returns the action cost"""
        action = self.ai_controller.act(self.player.coord)
        assert action != Action.No_Action, "AI chose {action=}"
        return action, self.action_interface.verify_and_get_cost(action)

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

    def creature_attack(self, attacker: Creature, target: Creature | Tile) -> tuple[bool, bool, int, int, Sequence[int]]:
        succeeds, damage = calc_melee_attack(attacker, target)
        died = False
        experience = 0
        levelups: Sequence[int] = []
        if isinstance(target, Creature):
            if damage:
                target.receive_damage(damage)
                if died := target.is_dead():
                    if target is self.player:
                        self.user_controller.process_feedback(AttackFeedback(attacker, target, succeeds, died, damage,
                                                                             0, ()))
                        self.end_game()
                    experience, levelups = self.creature_death(attacker, target)
        return succeeds, died, damage, experience, levelups

    def creature_death(self, attacker: Creature, target: Creature) -> tuple[int, Sequence[int]]:

        self.ai_controller.remove_creature_state(target)
        target.level.remove_creature(target)
        return attacker.gain_kill_xp(target)

    def end_game(self) -> NoReturn:
        sys.exit(0)

    def save_game(self) -> str:
        try:
            msg_str = state_store.save(self, self.game_name)
        except IOError as e:
            msg_str = str(e)
        return msg_str

    def update_view(self, creature: Visionary) -> None:
        """
        Update the vision set of the Visionary.
        """
        lvl = creature.level
        new_vision = ShadowCast.get_light_set(lvl.is_see_through, creature.coord, creature[Stat.SIGHT],
                                              lvl.rows, lvl.cols)
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
            'io',
            'action_interface',
            'ai_controller',
            'user_controller',
        )
        state = vars(self).copy()
        for item in exclude_state:
            del state[item]
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        vars(self).update(state)
