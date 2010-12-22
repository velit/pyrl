import curses

from creature import Creature
from char import Char
from tile import tiles
from io import io
from constants import *

class Player(Creature):
	"""da player object"""
	def __init__(self, game, level):
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

	def def_actions(self):
		a = {}

		a[curses.KEY_DOWN] = "move", S
		a[curses.KEY_LEFT] = "move", W
		a[curses.KEY_RIGHT] = "move", E
		a[curses.KEY_UP] = "move", N
		a[ord('+')] = "change_sight_range", 1
		a[ord('-')] = "change_sight_range", -1
		a[ord('.')] = "move", STOP
		a[ord('1')] = "move", SW
		a[ord('2')] = "move", S
		a[ord('3')] = "move", SE
		a[ord('4')] = "move", W
		a[ord('5')] = "move", STOP
		a[ord('6')] = "move", E
		a[ord('7')] = "move", NW
		a[ord('8')] = "move", N
		a[ord('9')] = "move", NE
		a[ord('<')] = "ascend",
		a[ord('>')] = "descend",
		a[ord('H')] = "los_highlight",
		a[ord('L')] = "loadgame",
		a[ord('Q')] = "endgame",
		a[ord('S')] = "savegame",
		a[ord('\x12')] = "redraw",
		a[ord('d')] = "debug",
		a[ord('k')] = "killall",
		a[ord('p')] = "path",

		self.actions = a

	def act(self):
		#self.l.drawmap()
		self.update_los()
		while True:
			c = io.getch(self.square.y, self.square.x)
			if c in self.actions:
				if self.exec_act(self.actions[c]):
					break
			else:
				if 0 < c < 256:
					c = chr(c)
					io.msg("Undefined command: '"+c+"'")
				else:
					io.msg("Undefined command key: "+str(c))

	def exec_act(self, act):
		return self.__getattribute__(act[0])(*act[1:])

	def move(self, dir):
		if dir == STOP:
			return True
		y, x = self.square.y + DY[dir], self.square.x + DX[dir]
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

	def descend(self):
		self.g.descend()
		return True

	def ascend(self):
		self.g.ascend()
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
		#self.l.drawmemory()
		#io.getch()
		#self.l.drawmap()
		#io.msg((self.square.getloc(), self.l.squares["ds"].getloc()))
		#io.l.drawline(self.square, self.l.squares["ds"])
		#self.redraw()

	def path(self):
		#io.drawpath(self.l.path(self.square, self.l.squares["ds"]))
		#io.msg(str(curses.A_NORMAL))
		#io.msg(io.rows)
		#io.msg(io.cols)
		#i = 0
		#for x in range(self.l.cols):
		#	i +=io.l.drawline(self.l.getsquare(25, 40),
		#self.l.getsquare(0, x))
		#for y in range(self.l.rows):
		#	i +=io.l.drawline(self.l.getsquare(25, 40),
		#			self.l.getsquare(y, self.l.cols-1))
		#io.msg(i)
		#io.msg(len(self.visibility-self.old_visibility))
		#io.l.drawline(self.l.getsquare(25, 40),
		#self.l.getsquare(44, 19))
		#io.l.drawline(self.l.getsquare(44, 19),
		#self.l.getsquare(25, 40))
		#io.msg(sorted((x.y, x.x) for x in self.visibility
		#if self.has_los(x)))
		io.msg(all(self.has_los(x) for x in self.visibility))
		for x in self.l.map:
			if not self.has_los(x): io.drawstar(x)
		io.getch()
		self.redraw()
		#pass
	
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
