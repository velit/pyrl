"""pyrl; Python roguelike by Tapani Kiiskinen."""
from __future__ import absolute_import, division, print_function, unicode_literals

import const.creature_actions as CC
import const.game as GAME
import const.stats as STAT
import mappings as MAPPING
import state_store
from ai import AI
from combat import get_melee_attack, get_combat_message
from config import debug
from fov import get_light_set
from generic_algorithms import add_vector
from templates.maps import get_world_template
from templates.player import Player
from user_input import UserInput
from window.window_system import WindowSystem
from world import World
from world_template import LevelNotFound


class Game(object):

    def __init__(self, game_name, cursor_lib):
        self.game_name = game_name
        self.turn_counter = 0
        self.current_vision = set()
        self.player = Player()
        self.ai = AI()
        self.world = World(get_world_template())

        self.reinit_transient_objects(cursor_lib)

        first_level, passage = self.world.get_first_level_info()
        self.move_creature_to_level(self.player, first_level, passage)
        self.vision_cache = None
        self.io.msg("{0} for help menu".format(MAPPING.HELP))

    def reinit_transient_objects(self, cursor_lib_callback):
        self.io = WindowSystem(cursor_lib_callback())
        self.user_input = UserInput(self, self.player, self.io)
        self.register_status_texts(self.player)

    def main_loop(self):
        player = self.player
        while True:
            creature, newcycle = player.level.turn_scheduler.get_actor_and_is_newcycle()

            #if newcycle:
            # do cycle based stuff

            if creature is player:
                if creature.can_act():
                    self.player_act()
                    self.turn_counter += 1
            else:
                self.ai.act_alert(self, creature, self.player.coord)

            creature.recover_energy()

    def player_act(self):
        level = self.player.level
        if debug.show_map:
            self.io.draw(level.get_wallhack_data(level.get_coord_iter()))
        self.update_view(self.player.level, self.player)
        self.user_input.get_user_input_and_act()

    def move_creature_to_level(self, creature, world_loc, passage):
        try:
            target_level = self.world.get_level(world_loc)
        except LevelNotFound:
            return False

        if creature.level is not None:
            creature.level.remove_creature(creature)

        target_level.add_creature_to_passage(creature, passage)

        if creature is self.player:
            self.current_vision = set()
            self.redraw()

        return True

    def creature_enter_passage(self, creature):
        level = creature.level
        if level.is_exit(creature.coord):
            passage = level.get_exit(creature.coord)
            dest_world_loc, dest_passage = level.get_destination_info(passage)
            if self.move_creature_to_level(creature, dest_world_loc, dest_passage):
                creature.update_energy(GAME.MOVEMENT_COST)
                return True
            self.io.msg("This passage doesn't seem to lead anywhere.")
        else:
            self.io.msg("There is no entrance.")
        return False

    def creature_move(self, creature, direction):
        level = creature.level
        if level.creature_can_move(creature, direction) and creature.can_act():
            target_coord = add_vector(creature.coord, direction)
            creature.update_energy(level.movement_cost(direction, target_coord))
            level.move_creature(creature, target_coord)
            return True
        else:
            if creature is not self.player:
                if not level.creature_can_move(creature, direction):
                    self.io.msg("Creature can't move there.")
                if not creature.can_act():
                    self.io.msg("Creature can't act now.")
            return False

    def creature_teleport(self, creature, target_coord):
        level = creature.level
        if level.is_passable(target_coord) and creature.can_act():
            creature.update_energy(GAME.MOVEMENT_COST)
            level.move_creature(creature, target_coord)
            return True
        else:
            if creature is not self.player:
                self.io.msg("Creature teleport failed.")
            return False

    def creature_swap(self, creature, direction):
        target_coord = add_vector(creature.coord, direction)
        level = creature.level
        if creature.can_act() and level.has_creature(target_coord):
            target_creature = level.get_creature(target_coord)
            if self.ai.willing_to_swap(target_creature, creature, self.player):
                energy_cost = level.movement_cost(direction, target_coord)
                creature.update_energy(energy_cost)
                target_creature.update_energy(energy_cost)
                level.swap_creature(creature, target_creature)
                return True

        if creature is not self.player:
            self.io.msg("Creature swap failed.")
        return False

    def creature_attack(self, creature, direction):
        level = creature.level
        if creature.can_act():
            creature.update_energy_action(CC.ATTACK)
            target_coord = add_vector(creature.coord, direction)
            if level.has_creature(target_coord):
                target = level.get_creature(target_coord)
            else:
                target = level.tiles[target_coord]
            succeeds, damage = get_melee_attack(creature.ar, creature.get_damage_info(), target.dr, target.pv)
            if damage:
                target.receive_damage(damage)
                died = target.is_dead()
            else:
                died = False
            personity = (creature is self.player, target is self.player)
            msg = get_combat_message(succeeds, damage, died, personity, creature.name, target.name)
            if died:
                self.creature_death(target)
            self.io.msg(msg)
            return True
        else:
            if creature is not self.player:
                self.io.msg("Creature attack failed.")
            return False

    def creature_death(self, creature):
        self.ai.remove_creature_state(creature)
        level = creature.level
        if creature is self.player:
            self.io.notify("You die...")
            self.endgame(dont_ask=True)
        level.remove_creature(creature)

    def register_status_texts(self, creature):
        self.io.s.add_element(STAT.DMG, lambda: "{}D{}+{}".format(*creature.get_damage_info()))
        self.io.s.add_element("HP", lambda: "{}/{}".format(creature.hp, creature.max_hp))
        self.io.s.add_element(STAT.SIGHT, lambda: creature.sight)
        self.io.s.add_element(STAT.AR, lambda: creature.ar)
        self.io.s.add_element(STAT.DR, lambda: creature.dr)
        self.io.s.add_element(STAT.PV, lambda: creature.pv)
        self.io.s.add_element(STAT.SPEED, lambda: creature.speed)
        self.io.s.add_element(STAT.ST, lambda: creature.st)
        self.io.s.add_element(STAT.DX, lambda: creature.dx)
        self.io.s.add_element(STAT.TO, lambda: creature.to)
        self.io.s.add_element(STAT.LE, lambda: creature.le)
        self.io.s.add_element(STAT.PE, lambda: creature.pe)
        self.io.s.add_element("Wloc", lambda: "{}/{}".format(*self.player.level.world_loc))
        self.io.s.add_element("Loc", lambda: "{0:02},{1:02}".format(*creature.coord))
        self.io.s.add_element("Turns", lambda: self.turn_counter)

    def endgame(self, dont_ask=True, message=""):
        self.io.msg(message)
        if dont_ask or self.io.ask("Do you wish to end the game? [y/N]") in GAME.YES:
            exit()

    def savegame(self, dont_ask=True):
        if dont_ask or self.io.ask("Do you wish to save the game? [y/N]") in GAME.YES:
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
        old = self.current_vision if not debug.show_map else set()
        new = get_light_set(level.is_see_through, creature.coord, creature.sight, level.rows, level.cols)
        mod = level.pop_modified_locations()
        level.update_visited_locations(new - old)

        out_of_sight_memory_data = level.get_memory_data(old - new)
        self.io.draw(out_of_sight_memory_data)

        new_visible_data = level.get_visible_data(new - (old - mod))
        self.io.draw(new_visible_data, debug.reverse)

        self.current_vision = new

    def redraw(self):
        self.io.l.clear()
        level = self.player.level
        if debug.show_map:
            self.io.draw(level.get_wallhack_data(level.get_coord_iter()))
        memory_data = level.get_memory_data(level.visited_locations)
        self.io.draw(memory_data)
        vision_data = level.get_visible_data(self.current_vision)
        self.io.draw(vision_data, debug.reverse)

    def __getstate__(self):
        exclude_state = ('user_input', 'io')
        state = self.__dict__.copy()
        for item in exclude_state:
            del state[item]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
