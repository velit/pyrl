import curses

from creature import Creature
from char import Char
from pio import io
from constants import DEFAULT, PASSAGE_UP, PASSAGE_DOWN
from const.directions import *

class Player(Creature):
	"""da player object"""
	def __init__(self, game, level=None):
		super(Player, self).__init__(game, level)
		self.name = "tappi"
		self.n = "god"
		self.ch = Char('@', "white")
		self.hp = 50
		self.dmg = 5

		self.register_status_texts()
		self.def_actions()

	def register_status_texts(self):
		io.s.add_element("hp", "HP: ", lambda: self.hp)
		io.s.add_element("sight", "sight: ", lambda: self.sight)
		io.s.add_element("turns", "TC: ", lambda: self.g.turn_counter)

	def def_actions(self):
		a = {}

		a[curses.KEY_DOWN] = "move_to_dir", (S, )
		a[curses.KEY_LEFT] = "move_to_dir", (W, )
		a[curses.KEY_RIGHT] = "move_to_dir", (E, )
		a[curses.KEY_UP] = "move_to_dir", (N, )
		a[ord('+')] = "change_sight_range", (1, )
		a[ord('-')] = "change_sight_range", (-1, )
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
			c = io.getch(self.square.y, self.square.x)
			if c in self.actions:
				if self.exec_act(self.actions[c]):
					break
			else:
				if 0 < c < 256:
					io.msg("Undefined command: '"+chr(c)+"'")
				else:
					io.msg("Undefined command key: "+str(c))

	def exec_act(self, act):
		return self.__getattribute__(act[0])(*act[1])

	def move_to_dir(self, dir):
		if dir == STOP:
			return True
		y, x = self.square.y + DY[dir], self.square.x + DX[dir]
		if self.move(y, x):
			return True
		else:
			io.msg("You can't move there.")
			return False

	def change_sight_range(self, amount):
		self.sight += amount
		return True

	def hit(self, creature):
		io.msg("You hit the "+creature.name+" for "+str(self.dmg)+
				" damage.")
		creature.lose_hp(self.dmg)

	def ascend(self):
		if self.square.ispassage() and self.square.tile.passage == PASSAGE_UP:
			self.enter()
		else:
			try:
				self.move(*self.l.getsquare(PASSAGE_UP).getloc())
				return True
			except KeyError:
				return False

	def descend(self):
		if self.square.ispassage() and self.square.tile.passage == PASSAGE_DOWN:
			self.enter()
		else:
			try:
				self.move(*self.l.getsquare(PASSAGE_DOWN).getloc())
				return True
			except KeyError:
				return False

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

	def path(self):
		io.msg("Shhhhhhh. Everything will be all right.")
	
	def los_highlight(self):
		if self.reverse == "":
			self.reverse = "r"
		elif self.reverse == "r":
			self.reverse = ""
		self.redraw()

	def killall(self):
		io.msg("Abrakadabra.")
		self.l.killall()
		return True
