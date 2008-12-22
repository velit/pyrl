import curses
import textwrap
from char import Char
from floor import Floor

class IO:
	class __impl:
		def __init__(self):
			self.w = curses.initscr()
			self.rows = self.w.getmaxyx()[0]
			self.cols = self.w.getmaxyx()[1]
			self.dy = 0
			self.dx = 0
			self.msgqueue = ""
			self.bufferLine = 0
			self.line1Size = 0
			self.line2Size = 0
			self.skipAll = False
			self.setColors()
			self.setFloors()
	
		def drawMap(self, map):
			for row in map.map:
				for square in row:
					self.w.addch(square.loc[0]+self.dy, square.loc[1]+self.dx, square.getChar(), square.getColor())

		def drawInterface(self, counter, id):
			self.addstr(-2, 0, "T: "+str(counter)+" ")
			self.addstr(-2, len(str(counter)+"T:  "), "ID: "+str(id)+" ")

		def drawLine(self, startSquare, targetSquare, char=None):
			if char is None:
				char = Char('*', self.colors["yellow"])
			x0, y0 = startSquare.loc
			x1, y1 = targetSquare.loc
			steep = abs(y1 - y0) > abs(x1 - x0)
			if steep:
				x0, y0 = y0, x0
				x1, y1 = y1, x1
			if x0 > x1:
				x0, x1 = x1, x0
				y0, y1 = y1, y0
			deltax = x1 - x0
			deltay = abs(y1 - y0)
			error = deltax / 2
			ystep = None
			y = y0
			if y0 < y1:
				ystep = 1
			else:
				ystep = -1
			for x in range(x0, x1):
				if steep:
					self.addch(y+self.dy, x+self.dx, char.symbol, char.color)
				else:
					self.addch(x+self.dy, y+self.dx, char.symbol, char.color)
				error -= deltay
				if error < 0:
					y += ystep
					error += deltax

		def drawTile(self, square):
			y,x=square.loc
			self.w.addch(y+self.dy, x+self.dx, square.getChar(), square.getColor())

		def moveCursor(self, square):
			y,x=square.loc
			self.w.move(y+self.dy, x+self.dx)

		def getch(self):
			c = self.w.getch()
			self.flushMsgArea()
			return c

		def getCharacters(self, list):
			c = None
			while c not in list:
				c = self.w.getch()
			self.flushMsgArea()
			return c

		def printMsg(self, str, color=curses.A_NORMAL):
			more = " (more)"
			if self.bufferLine == 0:
				if self.line1Size + len(str) + len(" ") < self.cols:
					self.w.addstr(0, self.line1Size, str, color)
					self.line1Size += len(str)+len(" ")
				elif str.find(' ') == -1 or not (self.line1Size + str.find(' ') + len(" ") < self.cols):
					self.bufferLine = 1
					self.printMsg(str)
				else:
					a = textwrap.wrap(str, self.cols-self.line1Size-len(" "))
					self.w.addstr(0, self.line1Size, a[0], color)
					self.line1Size += len(a[0]) + len(" ")
					self.bufferLine = 1
					self.printMsg(str.replace(a[0]+" ", "", 1))
			elif self.bufferLine == 1:
				if self.line2Size + len(str) + len(more) + len(" ") < self.cols:
					self.w.addstr(1, self.line2Size, str, color)
					self.line2Size += len(str)+len(" ")
				elif str.find(' ') == -1 or not (self.line2Size + str.find(' ') + len(" ") < self.cols):
					self.w.addstr(1, self.line2Size, more, color)
					self.line2Size += len(more+" ")
					if not self.skipAll:
						c = self.getCharacters([32,10])
						if c == 10:
							self.skipAll = True
					self.clearMsgs()
					self.printMsg(str)
				else:
					a = textwrap.wrap(str, self.cols-self.line2Size-len(more+" "))
					self.w.addstr(1, self.line2Size, a[0]+more, color)
					self.line2Size += len(a[0]) + len(more+" ")
					if not self.skipAll:
						c = self.getCharacters([32,10])
						if c == 10:
							self.skipAll = True
					self.clearMsgs()
					self.printMsg(str.replace(a[0]+" ", "", 1))

		def clearMsgs(self):
			if self.line1Size:
				self.w.move(0,0)
				for x in range(self.line1Size):
					self.w.addch(' ')
				self.line1Size = 0
			if self.line2Size:
				self.w.move(1,0)
				for x in range(self.line2Size):
					self.w.addch(' ')
				self.line2Size = 0

			self.bufferLine = 0

		def queueMsg(self, str):
			self.msgqueue += str+" "
		
		def printQueue(self):
			self.printMsg(self.msgqueue)
			self.msgqueue = ""

		def flushMsgArea(self):
			if self.skipAll:
				self.skipAll = False
			self.clearMsgs()

		def addstr(self, row, col, str, color=curses.A_NORMAL):
			if row < 0:
				row += self.rows
			if col < 0:
				col += self.cols
			self.w.addstr(row, col, str, color)

		def addch(self, row, col, ch, color=curses.A_NORMAL):
			if row < 0:
				row += self.rows
			if col < 0:
				col += self.cols
			self.w.addch(row, col, ch, color)
			
		def setColors(self):
			for x in range(7):
				curses.init_pair(x+1, x, 0)
			self.colors = {}

			self.colors["grey"] = curses.color_pair(0)
			self.colors["black_on_black"] = curses.color_pair(1)
			self.colors["red"] = curses.color_pair(2)
			self.colors["green"] = curses.color_pair(3)
			self.colors["yellow"] = curses.color_pair(4)
			self.colors["blue"] = curses.color_pair(5)
			self.colors["purple"] = curses.color_pair(6)
			self.colors["cyan"] = curses.color_pair(7)

			self.colors["white"] = curses.color_pair(0) | curses.A_BOLD
			self.colors["black"] = curses.color_pair(1) | curses.A_BOLD
			self.colors["light_red"] = curses.color_pair(2) | curses.A_BOLD
			self.colors["light_green"] = curses.color_pair(3) | curses.A_BOLD
			self.colors["light_yellow"] = curses.color_pair(4) | curses.A_BOLD
			self.colors["light_blue"] = curses.color_pair(5) | curses.A_BOLD
			self.colors["light_purple"] = curses.color_pair(6) | curses.A_BOLD
			self.colors["light_cyan"] = curses.color_pair(7) | curses.A_BOLD

		def setFloors(self):
			self.floors = {}
			self.floors["f"] = Floor("Dungeon Floor", Char('.'), True)
			self.floors["r"] = Floor("Dungeon Rock", Char('#'), False)
			self.floors["w"] = Floor("Wall", Char('#', self.colors["black"]), False)
			self.floors["ds"] = Floor("Down Staircase", Char('>'), True)
			self.floors["us"] = Floor("Up Staircase", Char('<'), True)

	__instance = None
	
	def __init__(self):
		if IO.__instance is None:
			IO.__instance = IO.__impl()

		self.__dict__["_IO_instance"] = IO.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)
