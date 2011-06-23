import curses

from creature import Creature
from char import Char
from pio import io
from const.game import DEFAULT, PASSAGE_UP, PASSAGE_DOWN
from const.directions import *


class Player(Creature):
	"""da player object"""

	def __init__(self, game, level=None):
		super().__init__(game, level)
		self.name = "tappi"
		self.n = "god"
		self.ch = Char('@', "white")
		self.stat.base_str = 50
		self.stat.base_con = 50

		self.register_status_texts()
		self.def_actions()

	def register_status_texts(self):
		io.s.add_element("hp", "HP: ", lambda: self.hp)
		io.s.add_element("sight", "sight: ", lambda: self.stat.sight)
		io.s.add_element("turns", "TC: ", lambda: self.g.turn_counter)
		io.s.add_element("loc", "Loc: ", lambda:self.l.world_loc)
		io.s.add_element("ar", "AR: ", lambda: self.stat.ar)
		io.s.add_element("dmg", "DMG: ", lambda: self.stat.dmg)
		io.s.add_element("dr", "DR: ", lambda: self.stat.dr)
		io.s.add_element("pv", "PV: ", lambda: self.stat.pv)

	def def_actions(self):
		a = {}

		a[curses.KEY_DOWN] = "move_to_dir", (S, )
		a[curses.KEY_LEFT] = "move_to_dir", (W, )
		a[curses.KEY_RIGHT] = "move_to_dir", (E, )
		a[curses.KEY_UP] = "move_to_dir", (N, )
		a[ord('.')] = "move_to_dir", (STOP, )
		a[ord('1')] = "move_to_dir", (SW, )
		a[ord('2')] = "move_to_dir", (S, )
		a[ord('3')] = "move_to_dir", (SE, )
		a[ord('4')] = "move_to_dir", (W, )
		a[ord('5')] = "move_to_dir", (STOP, )
		a[ord('6')] = "move_to_dir", (E, )
		a[ord('7')] = "move_to_dir", (NW, )
		a[ord('8')] = "move_to_dir", (N, )
		a[ord('9')] = "move_to_dir", (NE, )
		a[ord('<')] = "ascend", ()
		a[ord('>')] = "descend", ()
		a[ord('H')] = "los_highlight", ()
		a[ord('K')] = "killall", ()
		a[ord('L')] = "loadgame", ()
		a[ord('Q')] = "endgame", ()
		a[ord('S')] = "savegame", ()
		a[ord('\x12')] = "redraw", ()
		a[ord('d')] = "debug", ()
		a[ord('h')] = "move_to_dir", (W, )
		a[ord('i')] = "move_to_dir", (NE, )
		a[ord('j')] = "move_to_dir", (S, )
		a[ord('k')] = "move_to_dir", (N, )
		a[ord('l')] = "move_to_dir", (E, )
		a[ord('m')] = "move_to_dir", (SE, )
		a[ord('n')] = "move_to_dir", (SW, )
		a[ord('p')] = "path", ()
		a[ord('u')] = "move_to_dir", (NW, )

		self.actions = a

	def act(self):
		self.update_view()
		while True:
			c = io.getch(*self.getloc())
			if c in self.actions:
				if self.exec_act(self.actions[c]):
					break
			else:
				if 0 < c < 256:
					io.msg("Undefined command: '{}'".format(chr(c)))
				else:
					io.msg("Undefined command key: {}".format(c))

	def exec_act(self, act):
		function, params = act
		return getattr(self, function)(*params)

	def move_to_dir(self, dir):
		if dir == STOP:
			return True
		sy, sx = self.getloc()
		y, x = sy + DY[dir], sx + DX[dir]
		if self.move(y, x):
			return True
		else:
			io.msg("You can't move there.")

	def attack(self, creature):
		attack_succeeds, damage = self._attack(creature)
		if attack_succeeds:
			if damage > 0:
				io.msg("You hit the {} for {} damage.".format(creature.name, damage))
				creature.lose_hp(damage)
			else:
				io.msg("You fail to hurt the {}.".format(creature.name))
		else:
			io.msg("You miss the {}.".format(creature.name))

	def kill(self, square, msg):
		if square.creature is not None:
			io.msg(msg.format(square.creature.name))
			square.creature.die()

	def killall(self):
		io.msg("Abrakadabra.")
		self.l.killall()
		return True

	def ascend(self):
		s = self.getsquare()
		if s.isexit() and s.tile.exit_point == PASSAGE_UP:
			try:
				self.exit_level()
				return True
			except KeyError:
				io.msg("This passage doesn't seem to lead anywhere.")
		else:
			try:
				s = self.l.getsquare(entrance=PASSAGE_UP)
				self.kill(s, "")
				self.move(*s.getloc())
				return True
			except KeyError:
				io.msg("This level doesn't seem to have an upward passage.")

	def descend(self):
		s = self.getsquare()
		if s.isexit() and s.tile.exit_point == PASSAGE_DOWN:
			try:
				self.exit_level()
				return True
			except KeyError:
				io.msg("This passage doesn't seem to lead anywhere.")
		else:
			try:
				s = self.l.getsquare(entrance=PASSAGE_DOWN)
				self.kill(s, "")
				self.move(*s.getloc())
				return True
			except KeyError:
				io.msg("This level doesn't seem to have a downward passage.")

	def die(self):
		io.sel_getch("You die... [more]", char_list=DEFAULT)
		self.g.endgame(False)

	def endgame(self):
		self.g.endgame()

	def savegame(self):
		self.g.savegame()

	def loadgame(self):
		self.g.loadgame()

	def debug(self):
		io.msg((io.level_rows, io.level_cols))
		io.msg(self.getloc())

	def path(self):
		io.msg("Shhhhhhh. Everything will be all right.")

	def los_highlight(self):
		if self.reverse == "":
			self.reverse = "r"
		elif self.reverse == "r":
			self.reverse = ""
		self.redraw_view()
