import curses

from creature import Creature
from char import Char
from fov import doFov
from tile import tiles
from io import io
from colors import color

SW = 1; S = 2; SE = 3; W = 4; STOP = 5; E = 6; NW = 7; N = 8; NE = 9

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

		a[ord('>')] = self.descend
		a[ord('<')] = self.ascend
		a[curses.KEY_DOWN] = lambda: self.move(S)
		a[curses.KEY_LEFT] = lambda: self.move(W)
		a[curses.KEY_RIGHT] = lambda: self.move(E)
		a[curses.KEY_UP] = lambda: self.move(N)
		a[ord('1')] = lambda: self.move(SW)
		a[ord('2')] = lambda: self.move(S)
		a[ord('3')] = lambda: self.move(SE)
		a[ord('4')] = lambda: self.move(W)
		a[ord('5')] = lambda: self.move(STOP)
		a[ord('6')] = lambda: self.move(E)
		a[ord('7')] = lambda: self.move(NW)
		a[ord('8')] = lambda: self.move(N)
		a[ord('9')] = lambda: self.move(NE)

		a[ord('Q')] = self.game.endGame
		a[ord('S')] = self.game.saveGame

		self.actions = a

	def move(self, d):
		y,x = self.l.squares[self].y, self.l.squares[self].x
		ny = y
		nx = x

		if d in (NW,N,NE):
			ny -= 1
		if d in (SW,S,SE):
			ny += 1 
		if d in (NW,W,SW):
			nx -= 1
		if d in (NE,E,SE):
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

	def act(self):
		self.hp -= 1
		self.updateLos()
		while True:
			c = io.getch(self.l.squares[self].y, self.l.squares[self].x)
			if c in self.actions:
				if self.actions[c]():
					break
			else:
				if 0 <= c < 256:
					c = chr(c)
					io.queueMsg("Undefined command: '"+c+"'")
				else:
					io.queueMsg("Undefined command key: "+str(c))
