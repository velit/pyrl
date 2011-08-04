import curses
import sys
import const.directions as dirs

from pio import io
from const.game import PASSAGE_UP, PASSAGE_DOWN, PyrlException
from char import Char

direction_keys = {
	curses.KEY_DOWN: dirs.SO,
	curses.KEY_LEFT: dirs.WE,
	curses.KEY_RIGHT: dirs.EA,
	curses.KEY_UP: dirs.NO,
	ord('.'): dirs.STOP,
	ord('1'): dirs.SW,
	ord('2'): dirs.SO,
	ord('3'): dirs.SE,
	ord('4'): dirs.WE,
	ord('5'): dirs.STOP,
	ord('6'): dirs.EA,
	ord('7'): dirs.NW,
	ord('8'): dirs.NO,
	ord('9'): dirs.NE,
	ord('h'): dirs.WE,
	ord('i'): dirs.NE,
	ord('j'): dirs.SO,
	ord('k'): dirs.NO,
	ord('l'): dirs.EA,
	ord('m'): dirs.SE,
	ord('n'): dirs.SW,
	ord('u'): dirs.NW,
	}

class UserInput:
	def __init__(self):
		no_args, no_kwds = (), {}
		self.actions = {
			ord('<'): ("enter", (PASSAGE_UP, ), no_kwds),
			ord('>'): ("enter", (PASSAGE_DOWN, ), no_kwds),
			ord('Q'): ("endgame", no_args, no_kwds),
			ord('S'): ("savegame", no_args, no_kwds),
			ord('d'): ("debug", no_args, no_kwds),
			ord('L'): ("look", no_args, no_kwds),
			ord('Z'): ("z_command", no_args, no_kwds),
			ord('\x12'): ("redraw_view", no_args, no_kwds),
		}
		for key, value in direction_keys.items():
			self.actions[key] = ("act_to_dir", (value, ), no_kwds)

	def get_and_act(self, game, level, creature):
		c = io.getch(*level.get_coord(creature.loc))
		if c in self.actions:
			return self.execute_action(game, level, creature, self.actions[c])
		else:
			io.msg("Undefined key: {}".format(chr(c) if 0 < c < 256 else c))

	def execute_action(self, game, level, creature, act):
		function, args, keywords = act
		return getattr(sys.modules[__name__], function)(game, level, creature, *args, **keywords)

def act_to_dir(game, level, creature, direction):
	if direction == dirs.STOP:
		return True
	target_loc = level.get_relative_loc(creature.loc, direction)
	if level.move_creature(creature, target_loc):
		return True
	elif level.has_creature(target_loc):
		attack_succeeds, name, dies, damage = level.creature_attack(creature, target_loc)
		if attack_succeeds:
			if damage > 0:
				if dies:
					io.msg("You hit the {} for {} damage and kill it.".format(name, damage))
				else:
					io.msg("You hit the {} for {} damage.".format(name, damage))
			else:
				if dies:
					io.msg("You fail to hur the {}. The {} suddenly collapses!".format(name, name))
				else:
					io.msg("You fail to hurt the {}.".format(name))
		else:
			io.msg("You miss the {}.".format(name))
		return True
	else:
		io.msg("You can't move there.")
		return False

def z_command(game, level, creature):
	c = io.getch()
	if c == ord('Q'):
		game.endgame(ask=False)
	elif c == ord('Z'):
		game.savegame(ask=False)

def look(game, level, creature):
	loc = creature.loc
	drawline_flag = False
	while True:
		c = io.getch(*level.get_coord(loc))
		game.redraw()
		direction = dirs.STOP
		if c in direction_keys:
			direction = direction_keys[c]
		elif c == ord('d'):
			drawline_flag = not drawline_flag
		elif c in map(ord, "QqzZ "):
			break
		loc = level.get_relative_loc(loc, direction)
		io.msg(level.get_information(loc))
		if drawline_flag:
			io.drawline(level.get_coord(creature.loc), level.get_coord(loc), Char("*", "yellow"))
			io.msg("LoS: {}".format(level.check_los(creature.loc, loc)))

def endgame(game, level, creature, *a, **k):
	game.endgame(*a, **k)

def savegame(game, level, creature, *a, **k):
	game.savegame(*a, **k)

def debug(game, level, creature):
	c = io.getch()
	if c == ord('v'):
		game.flags.show_map = not game.flags.show_map
		game.redraw()
	elif c == ord('h'):
		game.flags.reverse = not game.flags.reverse
		game.redraw()
	elif c == ord('k'):
		for loc in tuple(level.creatures):
			if loc == creature.loc:
				continue
			else:
				level.remove_creature(loc)
		io.msg("Abrakadabra.")
	elif c == ord('p'):
		io.msg("pathing f, unimplemented")
	else:
		io.msg("Undefined debug key: {}".format(chr(c) if 0 < c < 256 else c))

def redraw_view(game, level, creature):
	game.redraw()

def enter(game, level, creature, passage):
	loc = game.player.loc
	if level.is_exit(loc) and level.get_exit(loc) == passage:
		try:
			game.enter_passage(level.world_loc, level.get_exit(loc))
		except PyrlException:
			io.msg("This passage doesn't seem to lead anywhere.")
	else:
		try:
			new_loc = level.get_passage_loc(passage)
		except KeyError:
			io.msg("This level doesn't seem to have a corresponding passage.")
		else:
			if not level.is_passable(new_loc):
				level.remove_creature(new_loc)
			level.move_creature(game.player, new_loc)
	return True
