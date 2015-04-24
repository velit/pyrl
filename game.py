"""pyrl; Python roguelike by Tapani Kiiskinen."""
from __future__ import absolute_import, division, print_function, unicode_literals

from config.game import GameConf
import state_store
from ai import AI
from config.debug import Debug
from creature.stats import Stat
from game_actions import GameActions
from fov import get_light_set
from config.mappings import Mapping
from game_data.maps import get_world_template
from game_data.player import Player
from user_input import UserInput
from window.window_system import WindowSystem
from world import World
from world_template import LevelNotFound


class Game(object):

    def __init__(self, game_name, cursor_lib):
        self.game_name = game_name
        self.turn_counter = 0
        self.player = Player()
        self.ai = AI()
        self.world = World(get_world_template())
        self.time = 0

        self.init_nonserialized_objects(cursor_lib)

        first_level, passage = self.world.get_first_level_info()
        self.move_creature_to_level(self.player, first_level, passage, turnscheduler_add=True)
        self.vision_cache = None
        self.io.msg("{0} for help menu".format(Mapping.Help))
        self.save_mark = False

    def init_nonserialized_objects(self, cursor_lib_callback):
        self.io = WindowSystem(cursor_lib_callback())
        self.user_input = UserInput(GameActions(self, self.player), self.io)
        self.register_status_texts(self.player)

    def main_loop(self):
        ai_game_actions = GameActions(self)
        while True:
            if self.save_mark:
                self.savegame(ask=False)
                self.save_mark = False

            creature, time_delta = self.player.level.turn_scheduler.advance_time()
            self.time += time_delta

            if creature is self.player:
                self.user_input.game_actions.clear_action()
                self.player_act()
                action_cost = self.user_input.game_actions.action_cost

                if action_cost > 0:
                    self.turn_counter += 1
            else:
                ai_game_actions.clear_action(and_associate_creature=creature)
                self.ai.act_alert(ai_game_actions, self.player.coord)
                action_cost = ai_game_actions.action_cost

            if action_cost < 0:
                raise ValueError("Negative cost actions are not allowed.")
            creature.level.turn_scheduler.add(creature, action_cost)

    def player_act(self):
        level = self.player.level
        if Debug.show_map:
            self.io.draw(level.get_wallhack_data(level.get_coord_iter()))
        self.update_view(level, self.player)
        self.user_input.get_user_input_and_act()

    def register_status_texts(self, creature):
        add_element = self.io.s.add_element
        add_element("Dmg",                      lambda: "{}D{}+{}".format(*creature.get_damage_info()))
        add_element("HP",                       lambda: "{}/{}".format(creature.hp, creature.max_hp))
        add_element(Stat.sight.value,           lambda: creature.sight)
        add_element(Stat.attack_rating.value,   lambda: creature.attack_rating)
        add_element(Stat.defense_rating.value,  lambda: creature.defense_rating)
        add_element(Stat.armor.value,           lambda: creature.armor)
        add_element(Stat.speed.value,           lambda: creature.speed)
        add_element(Stat.strength.value,        lambda: creature.strength)
        add_element(Stat.dexterity.value,       lambda: creature.dexterity)
        add_element(Stat.intelligence.value,    lambda: creature.intelligence)
        add_element(Stat.endurance.value,       lambda: creature.endurance)
        add_element(Stat.perception.value,      lambda: creature.perception)
        add_element("Wloc",                     lambda: "{}/{}".format(*self.player.level.world_loc))
        add_element("Loc",                      lambda: "{0:02},{1:02}".format(*creature.coord))
        add_element("Turns",                    lambda: self.turn_counter)
        add_element("Game Time",                lambda: self.time)
        add_element("Level Time",               lambda: self.player.level.turn_scheduler.time)

    def move_creature_to_level(self, creature, world_loc, passage, turnscheduler_add=False):
        try:
            target_level = self.world.get_level(world_loc)
        except LevelNotFound:
            return False

        if creature.level is not None:
            creature.level.remove_creature(creature, turnscheduler_remove=False)

        target_level.add_creature_to_passage(creature, passage, turnscheduler_add)

        try:
            creature.current_vision.clear()
        except AttributeError:
            pass
        else:
            self.redraw()

        return True

    def creature_death(self, creature):
        self.ai.remove_creature_state(creature)
        level = creature.level
        if creature is self.player:
            self.io.notify("You die...")
            self.endgame(ask=False)
        level.remove_creature(creature)

    def endgame(self, ask=True):
        if not ask or self.io.ask("Do you wish to end the game? [y/N]") in GameConf.YES:
            exit()

    def mark_save(self):
        self.save_mark = True

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

    def update_view(self, level, creature):
        """
        Update the current_vision set of the creature.

        This operation should only be done on creatures that have the .current_vision
        attribute ie. AdvancedCreatures for instance.
        """
        if Debug.show_map:
            creature.current_vision.clear()
        old = creature.current_vision
        new = get_light_set(level.is_see_through, creature.coord, creature.sight, level.rows, level.cols)
        mod = level.pop_modified_locations()
        level.update_visited_locations(new)

        out_of_sight_memory_data = level.get_memory_data(old - new)
        self.io.draw(out_of_sight_memory_data)

        new_visible_data = level.get_visible_data(new - (old - mod))
        self.io.draw(new_visible_data, Debug.reverse)

        creature.current_vision = new

    def redraw(self):
        self.io.l.clear()
        level = self.player.level
        if Debug.show_map:
            self.io.draw(level.get_wallhack_data(level.get_coord_iter()))
        memory_data = level.get_memory_data(level.visited_locations)
        self.io.draw(memory_data)
        vision_data = level.get_visible_data(self.player.current_vision)
        self.io.draw(vision_data, Debug.reverse)

    def __getstate__(self):
        exclude_state = ('user_input', 'io')
        state = self.__dict__.copy()
        for item in exclude_state:
            del state[item]
        return state

    def __setstate__(self, state):
        vars(self).update(state)
