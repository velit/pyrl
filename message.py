from textwrap import TextWrapper
import curses

class MessageBar:
	"""Handles the messaging bar system."""
	def __init__(self, window, io, more_str=" (more)"):
		self.w = window
		self.w.keypad(1)
		self.io = io
		self.lines, self.width = self.w.getmaxyx()
		self.msgqueue = ""
		self.cur_line = 0
		self.more_str=more_str
		self.wrapper = TextWrapper(width=(self.width - 1)) #accommodate for printing the newline character
		self.last_line_wrapper = TextWrapper(width=(self.width - len(self.more_str) - 1)) #accommodate for the more_str if the messages continue on the next page

	def update(self):
		self.printQueue()
		self.w.noutrefresh()

	def queueMsg(self, str):
		self.msgqueue += str+" "

	def clearMsgArea(self): #TODO perhaps only clear messages that are actually on screen, also implement a log history
		self.w.erase()
		self.cur_line = 0
	
	def getStr(self, str):
		self.clearMsgArea()
		self.w.addstr(0,0,str)
		curses.echo()
		a = self.w.getstr()
		self.w.addstr(a)
		self.w.getch()
		curses.noecho()
		return a

	def printQueue(self):
		str = self.msgqueue
		self.clearMsgArea()
		skip_all = False
		while True:
			if self.cur_line < self.lines - 1:
				if len(str) < self.width:
					self.w.addstr(self.cur_line, 0, str)
					break
				else:
					a = self.wrapper.wrap(str)
					self.w.addstr(self.cur_line, 0, a[0])
					str = " ".join(a[1:])
					self.cur_line += 1
			elif self.cur_line == self.lines - 1:
				if len(str) < self.width:
					self.w.addstr(self.cur_line, 0, str)
					break
				else:
					a = self.last_line_wrapper.wrap(str)
					self.w.addstr(self.cur_line, 0, a[0]+self.more_str)
					if not skip_all:
						c = self.getCharacters((ord('\n'), ord(' ')))
						if c == ord('\n'):
							skip_all = True
					str = " ".join(a[1:])
					self.cur_line = 0
					self.clearMsgArea()
		self.msgqueue = ""

	def getCharacters(self, list):
		c = None
		while c not in list:
			c = self.w.getch()
		return c
