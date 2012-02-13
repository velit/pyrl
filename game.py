import ai
import const.game as GAME
import const.creature_actions as CC
import state_store

from input_output import io
from player import Player
from level import Level
from user_input import UserInput
from fov import get_light_set
from world_file import WorldFile
from debug_flags import Flags
from combat import get_melee_attack, get_combat_message
from itertools import imap


class Game(object):

	def __init__(self):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""

		self.turn_counter = 0
		self.user_input = UserInput()
		self.old_visibility = set()
		self.levels = {}
		self.world_file = WorldFile()
		self.player = Player()
		self.flags = Flags()

		self.init_new_level(GAME.FIRST_LEVEL)
		self.cur_level = self.levels[GAME.FIRST_LEVEL]
		self.cur_level.add_creature(self.player)
		self.register_status_texts(self.player)

	def is_player(self, creature):
		return self.player is creature

	def register_status_texts(self, creature):
		#io.s.add_element("dmg", "DMG: ", lambda: "{}D{}+{}".format(*creature.get_damage_info()))
		#io.s.add_element("hp", "HP: ", lambda: "{}/{}".format(creature.hp, creature.max_hp))
		io.s.add_element("sight", "SR: ", lambda: creature.sight)
		io.s.add_element("turns", "TC: ", lambda: self.turn_counter)
		io.s.add_element("world_loc", "Loc: ", lambda: "{}/{}".format(*self.cur_level.world_loc))
		#io.s.add_element("ar", "AR: ", lambda: creature.ar)
		#io.s.add_element("dr", "DR: ", lambda: creature.dr)
		#io.s.add_element("pv", "PV: ", lambda: creature.pv)
		io.s.add_element("speed", "SP: ", lambda: creature.speed)
		io.s.add_element("coord", "Loc: ", lambda: creature.coord)
		io.s.add_element("target", "TA: ", lambda: creature.target_coord)
		io.s.add_element("chase_vector", "CV: ", lambda: creature.chase_vector)

	def enter_passage(self, origin_world_loc, origin_passage):
		instruction, d, i = self.world_file.get_passage_info(origin_world_loc, origin_passage)
		if instruction == GAME.SET_LEVEL:
			self.change_level((d, i))
		else:
			d, i = self.cur_level.world_loc
			if instruction == GAME.PREVIOUS_LEVEL:
				self.change_level((d, i - 1), GAME.PASSAGE_DOWN)
			elif instruction == GAME.NEXT_LEVEL:
				self.change_level((d, i + 1), GAME.PASSAGE_UP)

	def change_level(self, world_loc, passage):
		old_level = self.cur_level
		try:
			self.cur_level = self.levels[world_loc]
		except KeyError:
			self.init_new_level(world_loc)
			self.cur_level = self.levels[world_loc]
		old_level.remove_creature(self.player)
		self.cur_level.add_creature(self.player, self.cur_level.get_passage_coord(passage))
		self.redraw()

	def init_new_level(self, world_loc):
		level_file = self.world_file.pop_level_file(world_loc)
		danger_level = level_file.danger_level
		level_monster_list = self.world_file.get_level_monster_list(danger_level)
		self.levels[world_loc] = Level(world_loc, level_file, level_monster_list)

	def play(self):
		if self.cur_level.turn_scheduler.is_new_turn():
			pass

		creature = self.cur_level.turn_scheduler.get()
		creature.recover_energy()
		if self.is_player(creature):
			if creature.can_act():
				self.player_act()
				self.turn_counter += 1
		else:
			ai.act_alert(self, self.cur_level, creature, self.player.coord)

	def player_act(self):
		i = 0
		while True:
			self.draw()
			took_action = self.user_input.get_and_act(self, self.cur_level, self.player)
			if took_action:
				i += 1
			if i == 1:
				break

	def creature_move(self, level, creature, direction):
		if level.creature_can_move(creature, direction) and creature.can_act():
			target_coord = level.get_relative_coord(creature.coord, direction)
			creature.update_energy(level.movement_cost(direction, target_coord))
			level.move_creature(creature, target_coord)
			return True
		else:
			return False

	def creature_swap(self, level, creature, direction):
		target_coord = level.get_relative_coord(creature.coord, direction)
		if creature.can_act() and level.creature_is_swappable(target_coord):
			target_creature = level.get_creature(target_coord)
			energy_cost = level.movement_cost(direction, target_coord)
			creature.update_energy(energy_cost)
			target_creature.update_energy(energy_cost)
			level.swap_creature(creature, target_creature)
			return True
		else:
			return False

	def creature_attack(self, level, creature, direction):
		if creature.can_act():
			creature.update_energy_action(CC.ATTACK)
			target_coord = level.get_relative_coord(creature.coord, direction)
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
			player_matrix = imap(self.is_player, (creature, target))
			msg = get_combat_message(succeeds, damage, died, player_matrix, creature.name, target.name)
			if died:
				self.creature_death(level, target)
			io.msg(msg)
			return True
		else:
			return False

	def creature_death(self, level, creature):
		if self.is_player(creature):
			io.notify("You die...")
			self.endgame(False)
		level.remove_creature(creature)

	def endgame(self, ask=False, message=""):
		io.msg(message)
		if not ask:
			exit()
		if io.ask("Do you wish to end the game? [y/N]") in GAME.YES:
			exit()

	def savegame(self, ask=False):
		if not ask or io.ask("Do you wish to save the game? [y/N]") in GAME.YES:
			io.msg("Saving...")
			io.refresh()
			io.msg(state_store.save(self, "pyrl.svg"))

	def draw(self):
		level, creature = self.cur_level, self.player
		self.update_view(level, creature)
		if self.flags.show_map:
			self.redraw()

	def redraw(self):
		io.clear_level_buffer()
		level, creature = self.cur_level, self.player
		self.redraw_view(level, creature)
		if self.flags.show_map:
			io.draw(level.get_visible_data(level.get_coord_iter()))

	def update_view(self, level, creature):
		old = self.old_visibility
		new = get_light_set(level.is_see_through, creature.coord, creature.sight)
		mod = level.pop_modified_locations()
		level.update_visited_locations(new - old)

		out_of_sight_memory_data = level.get_memory_data(old - new)
		io.draw(out_of_sight_memory_data)

		new_visible_data = level.get_visible_data(new - (old - mod))
		io.draw(new_visible_data, self.flags.reverse)

		self.old_visibility = new

	def redraw_view(self, level, creature):
		self.old_visibility.clear()
		memory_data = level.get_memory_data(level.visited_locations)
		io.draw(memory_data)
		self.update_view(level, creature)
