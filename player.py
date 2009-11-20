import curses

from creature import Creature
from char import Char
from fov import doFov
from tile import tiles
from io import io
from colors import color

SW = 1; S = 2; SE = 3; W = 4; STOP = 5; E = 6; NW = 7; N = 8; NE = 9

class Player(Creature):

	def __init__(self, game):
		Creature.__init__(self)
		self.game = game
		self.ch = Char('@', color["white"])

		io.s.register("hp", "HP: ", lambda: self.hp)

		a = {}
		n = {}

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

		n[ord('Q')] = game.endGame
		n[ord('S')] = game.saveGame

		self.actions = a
		self.non_actions = n

	def move(self, d):
		y,x = self.game.cur_level.squares[self].y, self.game.cur_level.squares[self].x
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
		
		target_square = self.game.cur_level.getSquare(ny,nx)

		if target_square.passable():
			self.game.cur_level.moveCreature(self, target_square)
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
			io.queueMsg("You hit the "+creature.name+" and kill "+creature.n+".")
			self.game.cur_level.removeCreature(creature)

	def descend(self):
		self.game.descend()

	def ascend(self):
		self.game.ascend()

	def act(self, game):
		self.hp -= 1
		while True:
			doFov(self, self.game.cur_level)
			c = io.getch(self.game.cur_level.squares[self].y, self.game.cur_level.squares[self].x)
			if c in self.actions:
				io.clearLos()
				self.actions[c]()
				break
			elif c in self.non_actions:
				self.non_actions[c]()
			else:
				if 0 <= c < 256:
					c = chr(c)
					io.queueMsg("Undefined command: '"+c+"'")
				else:
					io.queueMsg("Undefined command key: "+str(c))
