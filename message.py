from window import Window
from textwrap import TextWrapper
import curses

class MessageBar(Window):
	"""Handles the messaging bar system."""
	def __init__(self, window, io, more_str=" (more)"):
		Window.__init__(self, window)
		self.io = io
		self.lines, self.width = self.w.getmaxyx()
		self.msgqueue = ""
		self.more_str=more_str

		#accommodate for printing the newline character
		self.wrapper = TextWrapper(width=(self.width - 1))

		#accommodate for the more_str if the messages continue on the next page
		self.last_line_wrapper = TextWrapper(width=(self.width - 
													len(self.more_str) - 1))

	def update(self):
		self.printQueue()
		#Window.update(self)
		self.w.noutrefresh()

	def queueMsg(self, str):
		self.msgqueue += str+" "

	def printQueue(self):
		self.clear()
		str = self.msgqueue
		cur_line = 0
		skip_all = False
		while True:
			if cur_line < self.lines - 1:
				if len(str) < self.width:
					self.w.addstr(cur_line, 0, str)
					break
				else:
					a = self.wrapper.wrap(str)
					self.w.addstr(cur_line, 0, a[0])
					str = " ".join(a[1:])
					cur_line += 1
			elif cur_line == self.lines - 1:
				if len(str) < self.width:
					self.w.addstr(cur_line, 0, str)
					break
				else:
					a = self.last_line_wrapper.wrap(str)
					self.w.addstr(cur_line, 0, a[0]+self.more_str)
					if not skip_all:
						c = self.getCharacters((ord('\n'), ord(' ')))
						if c == ord('\n'):
							skip_all = True
					str = " ".join(a[1:])
					cur_line = 0
					self.clear()
		self.msgqueue = ""
