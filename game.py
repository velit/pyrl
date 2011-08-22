import os
import pickle

import const.game as CG

from pio import io
from player import Player
from level import Level
from user_input import UserInput
from ai import AI
from fov import get_light_set
from world_file import WorldFile
from debug_flags import Flags


class Game:

	def __init__(self):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""

		self.turn_counter = 0
		self.user_input = UserInput()
		self.ai = AI()
		self.old_visibility = set()
		self.levels = {}
		self.world_file = WorldFile()
		self.player = Player()
		self.flags = Flags()

		self.init_new_level(CG.FIRST_LEVEL)
		self.cur_level = self.levels[CG.FIRST_LEVEL]
		self.cur_level.add_creature(self.player)
		self.register_status_texts()

	def register_status_texts(self):
		io.s.add_element("dmg", "DMG: ", lambda: "{}D{}+{}".format( *self.player.get_damage_info()))
		io.s.add_element("hp", "HP: ", lambda: "{}/{}".format(self.player.hp, self.player.max_hp))
		io.s.add_element("sight", "sight: ", lambda: self.player.sight)
		io.s.add_element("turns", "TC: ", lambda: self.turn_counter)
		io.s.add_element("loc", "Loc: ", lambda:self.cur_level.world_loc)
		io.s.add_element("ar", "AR: ", lambda: self.player.ar)
		io.s.add_element("dr", "DR: ", lambda: self.player.dr)
		io.s.add_element("pv", "PV: ", lambda: self.player.pv)
	
	def enter_passage(self, origin_world_loc, origin_passage):
		instruction, d, i = self.world_file.get_passage_info(origin_world_loc, origin_passage)
		if instruction == CG.SET_LEVEL:
			self.change_level((d, i))
		else:
			d, i = self.cur_level.world_loc
			if instruction == CG.PREVIOUS_LEVEL:
				self.change_level((d, i - 1), CG.PASSAGE_DOWN)
			elif instruction == CG.NEXT_LEVEL:
				self.change_level((d, i + 1), CG.PASSAGE_UP)

	def change_level(self, world_loc, passage):
		old_level = self.cur_level
		try:
			self.cur_level = self.levels[world_loc]
		except KeyError:
			self.init_new_level(world_loc)
			self.cur_level = self.levels[world_loc]
		old_level.remove_creature(self.player.loc)
		self.cur_level.add_creature(self.player, self.cur_level.get_passage_loc(passage))
		self.redraw()

	def init_new_level(self, world_loc):
		level_file = self.world_file.pop_level_file(world_loc)
		danger_level = level_file.danger_level
		level_monster_list = self.world_file.get_level_monster_list(danger_level)
		self.levels[world_loc] = Level(world_loc, level_file, level_monster_list)

	def play(self):
		game, level, player = self, self.cur_level, self.player
		creature = level.turn_scheduler.get()
		if creature == player:
			i = 0
			while True:
				self.draw()
				took_action = self.user_input.get_and_act(game, level, creature)
				if took_action:
					i += 1
					self.turn_counter += 1
				if i == 1:
					break
		else:
			self.ai.act(level, creature, player.loc)

	def endgame(self, ask=False):
		if not ask:
			exit()
		if io.sel_getch("Do you wish to end the game? [y/N]") in CG.YES:
			exit()

	def _save(self):
		save_path = os.path.join("data", "pyrl.svg")
		with open(save_path, "wb") as f:
			pickle.dump(self, f)
		io.msg("Savegame file size: {} bytes".format(os.path.getsize(save_path)))

	def savegame(self, ask=False):
		if not ask:
			self._save()
		elif io.sel_getch("Do you wish to save the game? [y/N]") in CG.YES:
			self._save()

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
			io.draw(level.get_visible_data(level.get_loc_iter()))

	def update_view(self, level, creature):
		old = self.old_visibility
		new = get_light_set(level.is_see_through, level.get_coord(creature.loc), creature.sight, level.cols)
		mod = level.pop_modified_locs()
		level.update_visited_locs(new - old)

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
