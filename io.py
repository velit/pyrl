import curses
import _curses
from message import MessageBar

class IO:
	class __impl:
		def __init__(self):
			self.w = curses.initscr()

			self.rows, self.cols = self.w.getmaxyx()
			self.msg_display_size = 2 #number of lines for the message display on the top of the screen
			self.status_size = 2 #number of lines for the status bar display at the bottom of the screen
			self.level_size = self.rows - self.msg_display_size - self.status_size #level size in lines
			self.level_dimensions = self.level_size, self.cols

			#message window
			self.m_w = curses.newwin(self.msg_display_size, 0, 0, 0)
			self.m_w.keypad(1)
			
			#status window
			self.s_w = curses.newwin(self.status_size, 0, self.rows - self.status_size, 0)
			self.s_w.keypad(1)
			
			#level window
			self.l_w = curses.newwin(self.level_size, 0, self.msg_display_size, 0)
			self.l_w.keypad(1)

			self.message_bar = MessageBar(self.m_w)
			
			self.setColors()
			self.visibility = []
			self.reverse = False

		def refreshWindows(self):
			self.message_bar.printQueue()
			self.m_w.noutrefresh()
			self.s_w.noutrefresh()
			self.l_w.noutrefresh()
			curses.doupdate()

		def drawMemoryMap(self, map):
			self.l_w.move(0,0)
			try:
				for row in map:
					for square in row:
						self.l_w.addch(square.y, square.x, square.getMemoryChar().symbol, square.getMemoryChar().color)

			except curses.error:
				pass #writing to the last cell of a window raises an exception because the automatic cursor move to the next cell is illegal, this works

		def drawMap(self, map):
			self.l_w.move(0,0)
			try:
				for row in map:
					for square in row:
						self.l_w.addch(square.y, square.x, square.getVisibleChar().symbol, square.getVisibleChar().color)

			except curses.error:
				pass #writing to the last cell of a window raises an exception because the automatic cursor move to the next cell is illegal, this works

		def drawChar(self, y, x, char):
			self.l_w.addch(y, x, char.symbol, char.color)

		def drawLos(self):
			if self.reverse:
				for square in self.visibility:
					self.l_w.addch(square.y, square.x, \
							square.getVisibleChar().symbol, square.getVisibleChar().color | self.colors["reverse"])
			else:
				for square in self.visibility:
					self.l_w.addch(square.y, square.x, \
							square.getVisibleChar().symbol, square.getVisibleChar().color)

		def clearLos(self):
			while True:
				try:
					square = self.visibility.pop()
				except IndexError:
					break
				self.l_w.addch(square.y, square.x, \
						square.getMemoryChar().symbol, square.getMemoryChar().color)

		def drawInterface(self, counter, id):
			self.s_w.addstr(0, 0, "T: "+str(counter)+" ")
			self.s_w.addstr(0, len(str(counter)+"T:  "), "ID: "+str(id)+" ")

		def getch(self, y=None, x=None):
			if y is not None and x is not None:
				self.l_w.move(y, x)	
			self.refreshWindows()
			c = self.l_w.getch()
			self.clearMsgArea()
			return c

		def getCharacters(self, list):
			c = None
			self.refreshWindows()
			while c not in list:
				c = self.l_w.getch()
			self.clearMsgArea()
			return c

		def queueMsg(self, str):
			self.message_bar.queueMsg(str)
		
		def clearMsgArea(self):
			self.message_bar.clearMsgArea()

		def drawLine(self, startSquare, targetSquare, char=None):
			if char is None:
				symbol = '*'
				color = self.colors["yellow"]
			else:
				symbol = char.symbol
				color = char.color
			x0, y0 = startSquare.y, startSquare.x
			x1, y1 = targetSquare.y, targetSquare.x
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
					self.l_w.addch(y, x, symbol, color)
				else:
					self.l_w.addch(x, y, symbol, color)
				error -= deltay
				if error < 0:
					y += ystep
					error += deltax
			self.l_w.getch()

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

			self.colors["blink"] = curses.A_BLINK
			self.colors["bold"] = curses.A_BOLD
			self.colors["dim"] = curses.A_DIM
			self.colors["reverse"] = curses.A_REVERSE
			self.colors["standout"] = curses.A_STANDOUT
			self.colors["underline"] = curses.A_UNDERLINE

	__instance = None
	
	def __init__(self):
		if IO.__instance is None:
			IO.__instance = IO.__impl()

		self.__dict__["_IO_instance"] = IO.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)
