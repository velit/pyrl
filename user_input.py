import curses
import sys
import const.directions as dirs

from pio import io
from const.game import PASSAGE_UP, PASSAGE_DOWN, PyrlException

class UserInput:
	def __init__(self):
		no_args, no_kwds = (), {}
		self.actions = {
			curses.KEY_DOWN: ("act_to_dir", (dirs.SO, ), no_kwds),
			curses.KEY_LEFT: ("act_to_dir", (dirs.WE, ), no_kwds),
			curses.KEY_RIGHT: ("act_to_dir", (dirs.EA, ), no_kwds),
			curses.KEY_UP: ("act_to_dir", (dirs.NO, ), no_kwds),
			ord('.'): ("act_to_dir", (dirs.STOP, ), no_kwds),
			ord('1'): ("act_to_dir", (dirs.SW, ), no_kwds),
			ord('2'): ("act_to_dir", (dirs.SO, ), no_kwds),
			ord('3'): ("act_to_dir", (dirs.SE, ), no_kwds),
			ord('4'): ("act_to_dir", (dirs.WE, ), no_kwds),
			ord('5'): ("act_to_dir", (dirs.STOP, ), no_kwds),
			ord('6'): ("act_to_dir", (dirs.EA, ), no_kwds),
			ord('7'): ("act_to_dir", (dirs.NW, ), no_kwds),
			ord('8'): ("act_to_dir", (dirs.NO, ), no_kwds),
			ord('9'): ("act_to_dir", (dirs.NE, ), no_kwds),
			ord('h'): ("act_to_dir", (dirs.WE, ), no_kwds),
			ord('i'): ("act_to_dir", (dirs.NE, ), no_kwds),
			ord('j'): ("act_to_dir", (dirs.SO, ), no_kwds),
			ord('k'): ("act_to_dir", (dirs.NO, ), no_kwds),
			ord('l'): ("act_to_dir", (dirs.EA, ), no_kwds),
			ord('m'): ("act_to_dir", (dirs.SE, ), no_kwds),
			ord('n'): ("act_to_dir", (dirs.SW, ), no_kwds),
			ord('u'): ("act_to_dir", (dirs.NW, ), no_kwds),
			ord('p'): ("path", no_args, no_kwds),
			ord('<'): ("enter", (PASSAGE_UP, ), no_kwds),
			ord('>'): ("enter", (PASSAGE_DOWN, ), no_kwds),
			ord('H'): ("los_highlight", no_args, no_kwds),
			ord('K'): ("killall", no_args, no_kwds),
			ord('Q'): ("endgame", no_args, no_kwds),
			ord('S'): ("savegame", no_args, no_kwds),
			ord('d'): ("debug", no_args, no_kwds),
			ord('Z'): ("z_command", no_args, no_kwds),
			ord('\x12'): ("redraw_view", no_args, no_kwds),
		}

	def get_and_act(self, game, level, creature):
		c = io.getch(*level.get_coord(creature.loc))
		if c in self.actions:
			return self.execute_action(game, level, creature, self.actions[c])
		else:
			if 0 < c < 256:
				io.msg("Undefined key: '{}'".format(chr(c)))
			else:
				io.msg("Undefined key: {}".format(c))

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

def killall(game, level, creature):
	for loc in tuple(level.creatures):
		if loc == creature.loc:
			continue
		else:
			level.remove_creature(loc)
	io.msg("Abrakadabra.")
	return True

def endgame(game, level, creature, *a, **k):
	game.endgame(*a, **k)

def savegame(game, level, creature, *a, **k):
	game.savegame(*a, **k)

def debug(game, level, creature):
	io.clear_level_buffer()

def path(game, level, creature):
	io.msg("Shhhhhhh. Everything will be all right.")

def redraw_view(game, level, creature):
	game.redraw()

def los_highlight(game, level, creature):
	game.reverse = not game.reverse

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
