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
from main import io
from templates.maps import get_world_template
from templates.player import Player
from user_input import UserInput
from world import World
from world_template import LevelNotFound


# Intentionally global due to Game getting pickled
user_input = UserInput()


class Game(object):

    def __init__(self):
        """pyrl; Python roguelike by Tapani Kiiskinen."""
        self.turn_counter = 0
        self.current_vision = set()
        self.player = Player()
        self.ai = AI()
        self.world = World(get_world_template())

        first_level, passage = self.world.get_first_level_info()
        self.move_creature_to_level(self.player, first_level, passage)
        self.register_status_texts(self.player)
        self.vision_cache = None

        io.msg("{0} for help menu".format(MAPPING.HELP))

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
            io.draw(level.get_wallhack_data(level.get_coord_iter()))
        self.update_view(self.player.level, self.player)
        user_input.get_user_input_and_act(self, self.player)

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
            io.msg("This passage doesn't seem to lead anywhere.")
        else:
            io.msg("There is no entrance.")
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
                    io.msg("Creature can't move there.")
                if not creature.can_act():
                    io.msg("Creature can't act now.")
            return False

    def creature_teleport(self, creature, target_coord):
        level = creature.level
        if level.is_passable(target_coord) and creature.can_act():
            creature.update_energy(GAME.MOVEMENT_COST)
            level.move_creature(creature, target_coord)
            return True
        else:
            if creature is not self.player:
                io.msg("Creature teleport failed.")
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
            io.msg("Creature swap failed.")
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
            io.msg(msg)
            return True
        else:
            if creature is not self.player:
                io.msg("Creature attack failed.")
            return False

    def creature_death(self, creature):
        self.ai.remove_creature_state(creature)
        level = creature.level
        if creature is self.player:
            io.notify("You die...")
            self.endgame(dont_ask=True)
        level.remove_creature(creature)

    def register_status_texts(self, creature):
        io.s.add_element(STAT.DMG, lambda: "{}D{}+{}".format(*creature.get_damage_info()))
        io.s.add_element("HP", lambda: "{}/{}".format(creature.hp, creature.max_hp))
        io.s.add_element(STAT.SIGHT, lambda: creature.sight)
        io.s.add_element(STAT.AR, lambda: creature.ar)
        io.s.add_element(STAT.DR, lambda: creature.dr)
        io.s.add_element(STAT.PV, lambda: creature.pv)
        io.s.add_element(STAT.SPEED, lambda: creature.speed)
        io.s.add_element(STAT.ST, lambda: creature.st)
        io.s.add_element(STAT.DX, lambda: creature.dx)
        io.s.add_element(STAT.TO, lambda: creature.to)
        io.s.add_element(STAT.LE, lambda: creature.le)
        io.s.add_element(STAT.PE, lambda: creature.pe)
        io.s.add_element("Wloc", lambda: "{}/{}".format(*self.player.level.world_loc))
        io.s.add_element("Loc", lambda: "{0:02},{1:02}".format(*creature.coord))
        io.s.add_element("Turns", lambda: self.turn_counter)

    def endgame(self, dont_ask=True, message=""):
        io.msg(message)
        if dont_ask or io.ask("Do you wish to end the game? [y/N]") in GAME.YES:
            exit()

    def savegame(self, dont_ask=True):
        if dont_ask or io.ask("Do you wish to save the game? [y/N]") in GAME.YES:
            io.msg("Saving...")
            io.refresh()
            io.msg(state_store.save(self, "pyrl.svg"))

    def update_view(self, level, creature):
        old = self.current_vision if not debug.show_map else set()
        new = get_light_set(level.is_see_through, creature.coord, creature.sight, level.rows, level.cols)
        mod = level.pop_modified_locations()
        level.update_visited_locations(new - old)

        out_of_sight_memory_data = level.get_memory_data(old - new)
        io.draw(out_of_sight_memory_data)

        new_visible_data = level.get_visible_data(new - (old - mod))
        io.draw(new_visible_data, debug.reverse)

        self.current_vision = new

    def redraw(self):
        io.l.clear()
        level = self.player.level
        if debug.show_map:
            io.draw(level.get_wallhack_data(level.get_coord_iter()))
        memory_data = level.get_memory_data(level.visited_locations)
        io.draw(memory_data)
        vision_data = level.get_visible_data(self.current_vision)
        io.draw(vision_data, debug.reverse)
