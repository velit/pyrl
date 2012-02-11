import curses
import sys
import const.directions as DIRS
import const.game as GAME
import const.debug as D

from pio import io
from char import Char
from itertools import imap

direction_map = {
		curses.KEY_LEFT: DIRS.WE,
		curses.KEY_DOWN: DIRS.SO,
		curses.KEY_UP: DIRS.NO,
		curses.KEY_RIGHT: DIRS.EA,
		ord(u'1'): DIRS.SW,
		ord(u'2'): DIRS.SO,
		ord(u'3'): DIRS.SE,
		ord(u'4'): DIRS.WE,
		ord(u'5'): DIRS.STOP,
		ord(u'6'): DIRS.EA,
		ord(u'7'): DIRS.NW,
		ord(u'8'): DIRS.NO,
		ord(u'9'): DIRS.NE,
		ord(u'h'): DIRS.WE,
		ord(u'j'): DIRS.SO,
		ord(u'k'): DIRS.NO,
		ord(u'l'): DIRS.EA,
		ord(u'.'): DIRS.STOP,
		ord(u'u'): DIRS.NW,
		ord(u'i'): DIRS.NE,
		ord(u'n'): DIRS.SW,
		ord(u'm'): DIRS.SE,
}

class UserInput(object):
	def __init__(self):
		no_args, no_kwds = (), {}
		self.actions = {
			ord(u'<'): (u"enter", (GAME.PASSAGE_UP, ), no_kwds),
			ord(u'>'): (u"enter", (GAME.PASSAGE_DOWN, ), no_kwds),
			ord(u'Q'): (u"endgame", no_args, no_kwds),
			ord(u'S'): (u"savegame", no_args, no_kwds),
			ord(u'q'): (u"look", no_args, no_kwds),
			ord(u'Z'): (u"z_command", no_args, no_kwds),
			ord(u'a'): (u"attack", no_args, no_kwds),
			ord(u'd'): (u"debug", no_args, no_kwds),
			ord(u'\x12'): (u"redraw_view", no_args, no_kwds),
		}
		for key, value in direction_map.items():
			self.actions[key] = (u"act_to_dir", (value, ), no_kwds)

	def get_and_act(self, game, level, creature):
		c = io.getch()
		if c in self.actions:
			return self.execute_action(game, level, creature, self.actions[c])
		else:
			io.msg(u"Undefined key: {}".format(unichr(c) if 0 < c < 256 else c))

	def execute_action(self, game, level, creature, act):
		function, args, keywords = act
		return getattr(sys.modules[__name__], function)(game, level, creature, *args, **keywords)

def act_to_dir(game, level, creature, direction):
	target_coord = level.get_relative_coord(creature.coord, direction)
	if game.creature_move(level, creature, direction):
		return True
	elif level.has_creature(target_coord):
		game.creature_attack(level, creature, direction)
		return True
	else:
		io.msg(u"You can't move there.")
		return False

def z_command(game, level, creature):
	c = io.getch()
	if c == ord(u'Q'):
		game.endgame(ask=False)
	elif c == ord(u'Z'):
		game.savegame(ask=False)

def look(game, level, creature):
	coord = creature.coord
	drawline_flag = False
	direction = DIRS.STOP
	while True:
		coord = level.get_relative_coord(coord, direction)
		io.msg(level.look_information(coord))
		if drawline_flag:
			io.drawline(level.get_coord(creature.coord), coord, Char(u"*", u"yellow"))
			io.msg(u"LoS: {}".format(level.check_los(creature.coord, coord)))
		c = io.getch(coord)
		game.redraw()
		direction = DIRS.STOP
		if c in direction_map:
			direction = direction_map[c]
		elif c == ord(u'd'):
			drawline_flag = not drawline_flag
		elif c == ord(u'b'):
			from generic_algorithms import bresenham
			for coord in bresenham(level.get_coord(creature.coord), coord):
				io.msg(coord)
		elif c == ord(u's'):
			if level.has_creature(coord):
				game.register_status_texts(level.get_creature(coord))
		elif c in imap(ord, u"QqzZ "):
			break

def endgame(game, level, creature, *a, **k):
	game.endgame(*a, **k)

def savegame(game, level, creature, *a, **k):
	game.savegame(*a, **k)

def attack(game, level, creature):
	c = io.sel_getch(u"Specify attack direction:", GAME.DEFAULT | set(direction_keys))
	if c in direction_map:
		game.creature_attack(level, creature, direction_map[c])
		return True

def debug(game, level, creature):
	c = io.getch_print(u"Avail cmds: vclbdhkp")
	if c == ord(u'v'):
		game.flags.show_map = not game.flags.show_map
		game.redraw()
		io.msg(u"Show map set to {}".format(game.flags.show_map))
	elif c == ord(u'c'):
		D.CROSS = not D.CROSS
		io.msg(u"Path heuristic cross set to {}".format(D.CROSS))
	elif c == ord(u'l'):
		GAME.LEVEL_TYPE = u"arena" if GAME.LEVEL_TYPE == u"dungeon" else u"dungeon"
		io.msg(u"Level type set to {}".format(GAME.LEVEL_TYPE))
	elif c == ord(u'b'):
		io.draw_block((4,4))
	elif c == ord(u'd'):
		D.PATH = not D.PATH
		io.msg(u"Path debug set to {}".format(D.PATH))
	elif c == ord(u'h'):
		game.flags.reverse = not game.flags.reverse
		game.redraw()
		io.msg(u"Reverse set to {}".format(game.flags.reverse))
	elif c == ord(u'k'):
		creature_list = list(level.creatures.values())
		creature_list.remove(creature)
		for i in creature_list:
			level.remove_creature(i)
		io.msg(u"Abrakadabra.")
	elif c == ord(u'p'):
		passage_up = level.get_passage_coord(GAME.PASSAGE_UP)
		passage_down = level.get_passage_coord(GAME.PASSAGE_DOWN)
		io.draw_path(level.path(passage_up, passage_down))
	else:
		io.msg(u"Undefined debug key: {}".format(unichr(c) if 0 < c < 256 else c))

def redraw_view(game, level, creature):
	game.redraw()

def enter(game, level, creature, passage):
	coord = game.player.coord
	if level.is_exit(coord) and level.get_exit(coord) == passage:
		try:
			game.enter_passage(level.world_loc, level.get_exit(coord))
		except GAME.PyrlException:
			io.msg(u"This passage doesn't seem to lead anywhere.")
	else:
		try:
			new_coord = level.get_passage_coord(passage)
		except KeyError:
			io.msg(u"This level doesn't seem to have a corresponding passage.")
		else:
			if not level.is_passable(new_coord):
				level.remove_creature(level.get_creature(new_coord))
			level.move_creature(game.player, new_coord)
	return True
