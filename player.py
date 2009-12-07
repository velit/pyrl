import curses

from creature import Creature
from char import Char
from fov import doFov
from tile import tiles
from io import io
from colors import color

SW = 1; S = 2; SE = 3; W = 4; STOP = 5; E = 6; NW = 7; N = 8; NE = 9
UP = (NW, N, NE)
DOWN = (SW, S, SE)
LEFT = (SW, W, NW)
RIGHT = (SE, E, NE)

class Player(Creature):
	def __init__(self, level, game):
		Creature.__init__(self, level)
		self.game = game
		self.name = "tappi"
		self.n = "god"
		self.ch = Char('@', color["white"])

		self.register_status_texts()
		self.def_actions()

	def register_status_texts(self):
		io.s.register("hp", "HP: ", lambda: self.hp)

	def def_actions(self):
		a = {}

		a[ord('>')] = "descend",
		a[ord('<')] = "ascend",
		a[ord('1')] = "move", SW
		a[ord('2')] = "move", S
		a[ord('3')] = "move", SE
		a[ord('4')] = "move", W
		a[ord('5')] = "move", STOP
		a[ord('6')] = "move", E
		a[ord('7')] = "move", NW
		a[ord('8')] = "move", N
		a[ord('9')] = "move", NE
		a[curses.KEY_UP] = "move", N
		a[curses.KEY_DOWN] = "move", S
		a[curses.KEY_LEFT] = "move", W
		a[curses.KEY_RIGHT] = "move", E

		a[ord('Q')] = "endgame",
		a[ord('S')] = "savegame",
		a[ord('L')] = "loadgame",

		self.actions = a

	def exec_act(self, act):
		if len(act) == 1:
			return getattr(self, act[0])()
		elif len(act) == 2:
			return getattr(self, act[0])(act[1])

	def move(self, d):
		y,x = self.l.squares[self].y, self.l.squares[self].x
		ny = y
		nx = x

		if d in UP:
			ny -= 1
		if d in DOWN:
			ny += 1 
		if d in LEFT:
			nx -= 1
		if d in RIGHT:
			nx += 1
		if d == STOP:
			return True
		
		target_square = self.l.getSquare(ny,nx)

		if target_square.passable():
			self.l.moveCreature(self, target_square)
			return True
		elif target_square.creature is not None:
			self.hit(target_square.creature)
			return True
		else:
			io.queueMsg("You can't move there.")
			return False

	def hit(self, creature):
		creature.hp -= 25
		if creature.hp > 0:
			io.queueMsg("You hit the "+creature.name+" and wound "+creature.n+".")
		else:
			creature.die()
			io.queueMsg("You hit the "+creature.name+" and kill "+creature.n+".")

	def descend(self):
		self.game.descend()
		return True

	def ascend(self):
		self.game.ascend()
		return True

	def endgame(self):
		self.game.endgame()

	def savegame(self):
		self.game.savegame()

	def loadgame(self):
		self.game.loadgame()

	def act(self):
		self.hp -= 1
		self.updateLos()
		while True:
			c = io.getch(self.l.squares[self].y, self.l.squares[self].x)
			if c in self.actions:
				if self.exec_act(self.actions[c]):
					break
			else:
				if 0 < c < 256:
					c = chr(c)
					io.queueMsg("Undefined command: '"+c+"'")
				else:
					io.queueMsg("Undefined command key: "+str(c))
