import curses

from creature import Creature
from char import Char
from tile import tiles
from io import io
from constants import DIR, DEFAULT, PASSAGE_UP, PASSAGE_DOWN

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

		a[curses.KEY_DOWN] = "move", (DIR.S, )
		a[curses.KEY_LEFT] = "move", (DIR.W, )
		a[curses.KEY_RIGHT] = "move", (DIR.E, )
		a[curses.KEY_UP] = "move", (DIR.N, )
		a[ord('+')] = "change_sight_range", (1, )
		a[ord('-')] = "change_sight_range", (-1, )
		a[ord('1')] = "move", (DIR.SW, )
		a[ord('n')] = "move", (DIR.SW, )
		a[ord('2')] = "move", (DIR.S, )
		a[ord('j')] = "move", (DIR.S, )
		a[ord('3')] = "move", (DIR.SE, )
		a[ord('m')] = "move", (DIR.SE, )
		a[ord('4')] = "move", (DIR.W, )
		a[ord('h')] = "move", (DIR.W, )
		a[ord('5')] = "move", (DIR.STOP, )
		a[ord('.')] = "move", (DIR.STOP, )
		a[ord('6')] = "move", (DIR.E, )
		a[ord('l')] = "move", (DIR.E, )
		a[ord('7')] = "move", (DIR.NW, )
		a[ord('u')] = "move", (DIR.NW, )
		a[ord('8')] = "move", (DIR.N, )
		a[ord('k')] = "move", (DIR.N, )
		a[ord('9')] = "move", (DIR.NE, )
		a[ord('i')] = "move", (DIR.NE, )
		a[ord('<')] = "ascend", ()
		a[ord('>')] = "descend", ()
		a[ord('H')] = "los_highlight", ()
		a[ord('L')] = "loadgame", ()
		a[ord('Q')] = "endgame", ()
		a[ord('S')] = "savegame", ()
		a[ord('\x12')] = "redraw", ()
		a[ord('d')] = "debug", ()
		a[ord('K')] = "killall", ()
		a[ord('p')] = "path", ()

		self.actions = a

	def act(self):
		self.update_los()
		self.l.drawmap()
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

	def move(self, dir):
		if dir == DIR.STOP:
			return True
		y, x = self.square.y + DIR.DY[dir], self.square.x + DIR.DX[dir]
		if self.l.legal_yx(y, x):
			targetsquare = self.l.getsquare(y,x)
			if targetsquare.passable():
				self.l.movecreature(self, targetsquare)
				return True
			elif targetsquare.creature is not None:
				self.hit(targetsquare.creature)
				return True
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

	def descend(self):
		if self.square.ispassage() and self.square.tile.passage == PASSAGE_DOWN:
			self.enter()

	def enter(self):
		if self.square.ispassage():
			self.g.enter(self.square.tile.passage)
			return True

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

	def redraw(self):
		self.g.redraw()

	def killall(self):
		io.msg("Abrakadabra.")
		self.l.killall()
		return True
