import os
import pickle

from pio import io
from player import Player
from level import Level
from user_input import UserInput
from fov import get_light_set
from world_file import WorldFile

from const.game import DEBUG, YES
from const.game import DUNGEON, FIRST_LEVEL
from const.game import SET_LEVEL, PREVIOUS_LEVEL, NEXT_LEVEL
from const.game import PASSAGE_UP, PASSAGE_DOWN


class Game:

	def __init__(self):
		"""pyrl; Python roguelike by Tapani Kiiskinen"""

		self.reverse = False
		self.turn_counter = 0
		self.user_input = UserInput()
		self.old_visibility = set()
		self.levels = {}
		self.world_file = WorldFile()
		self.player = Player()

		self.init_new_level(FIRST_LEVEL)
		self.cur_level = self.levels[FIRST_LEVEL]
		self.cur_level.addcreature(self.player)
		self.register_status_texts()

	def register_status_texts(self):
		io.s.add_element("dmg", "DMG: ", lambda: "{}D{}+{}".format( *self.player.stat.get_damage_info()))
		io.s.add_element("hp", "HP: ", lambda: "{}/{}".format(self.player.hp, self.player.stat.max_hp))
		io.s.add_element("sight", "sight: ", lambda: self.player.stat.sight)
		io.s.add_element("turns", "TC: ", lambda: self.turn_counter)
		io.s.add_element("loc", "Loc: ", lambda:self.cur_level.world_loc)
		io.s.add_element("ar", "AR: ", lambda: self.player.stat.ar)
		io.s.add_element("dr", "DR: ", lambda: self.player.stat.dr)
		io.s.add_element("pv", "PV: ", lambda: self.player.stat.pv)
	
	def enter_passage(self, origin_world_loc, origin_passage):
		instruction, d, i = self.world_file.get_passage_info(origin_world_loc, origin_passage)
		if instruction == SET_LEVEL:
			self.change_level((d, i))
		else:
			d, i = self.cur_level.world_loc
			if instruction == PREVIOUS_LEVEL:
				self.change_level((d, i - 1), PASSAGE_DOWN)
			elif instruction == NEXT_LEVEL:
				self.change_level((d, i + 1), PASSAGE_UP)

	def change_level(self, world_loc, passage):
		old_level = self.cur_level
		try:
			self.cur_level = self.levels[world_loc]
		except KeyError:
			self.init_new_level(world_loc)
			self.cur_level = self.levels[world_loc]
		old_level.removecreature(self.player.loc)
		self.cur_level.addcreature(self.player, self.cur_level.get_passage_loc(passage))
		self.redraw()

	def init_new_level(self, world_loc):
		level_file = self.world_file.get_level_file(world_loc)
		danger_level = level_file.danger_level
		level_monster_list = self.world_file.get_level_monster_list(danger_level)
		self.levels[world_loc] = Level(self, world_loc, level_file, level_monster_list)

	def play(self):
		creature = self.cur_level.turn_scheduler.get()
		if creature == self.player:
			while True:
				self.draw()
				took_action = self.user_input.get_and_act(self, self.cur_level, self.player)
				if took_action:
					break
		self.turn_counter += 1

	def endgame(self, ask=False):
		if not ask:
			exit()
		if io.sel_getch("Do you wish to end the game? [y/N]") in YES:
			exit()

	def _save(self):
		path = os.path.join("data", "pyrl.svg")
		with open(path, "wb") as f:
			pickle.dump(self, f)
		io.msg("Savegame file size: {} bytes".format(os.path.getsize(path)))

	def savegame(self, ask=False):
		if not ask:
			self._save()
		elif io.sel_getch("Do you wish to save the game? [y/N]") in YES:
			self._save()

	def draw(self):
		level, creature = self.cur_level, self.player
		self.update_view(level, creature)
		#io.drawlevel(level)

	def redraw(self):
		level, creature = self.cur_level, self.player
		self.redraw_view(level, creature)
		#io.drawlevel(level)

	def update_view(self, level, creature):
		old = self.old_visibility
		new = get_light_set(level.see_through, level.get_coord(creature.loc), creature.stat.sight, level.cols)
		mod = level.pop_modified_locs()
		level.update_visited_locs(new - old)

		out_of_sight_memory_data = level.get_memory_data(old - new)
		io.level_draw(out_of_sight_memory_data)

		new_visible_data = level.get_visible_data(new - (old - mod))
		io.level_draw(new_visible_data, self.reverse)

		self.old_visibility = new

	def redraw_view(self, level, creature):
		io.clear_level_buffer()
		self.old_visibility.clear()
		memory_data = level.get_memory_data(level.visited_locations)
		io.level_draw(memory_data)
		self.update_view(level, creature)
