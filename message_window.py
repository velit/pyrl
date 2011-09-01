import curses

import const.game as CG

from window import Window
from textwrap import TextWrapper


class MessageBar(Window):
	"""Handles the messaging bar system."""

	def __init__(self, window):
		super().__init__(window)

		self.msgqueue = ""

		#accommodate for printing the newline character
		self.wrapper = TextWrapper(width=(self.cols))

		#accommodate for the more_str if the messages continue on the next page
		self.last_line_wrapper = TextWrapper(width=(self.cols - len(CG.MORE_STR) - 1))

	def update(self):
		self.print_queue()
		Window.update(self)

	def queue_msg(self, obj):
		msg = str(obj)
		if len(msg) > 0:
			self.msgqueue += msg + " "

	def print_queue(self):
		self.clear()
		msg = self.msgqueue
		cur_line = 0
		skip_all = False
		while True:
			if cur_line < self.rows - 1:
				if len(msg) <= self.cols:
					self.w.addstr(cur_line, 0, msg)
					break
				else:
					a = self.wrapper.wrap(msg)
					self.w.addstr(cur_line, 0, a[0])
					msg = " ".join(a[1:])
					cur_line += 1
			elif cur_line == self.rows - 1:
				if len(msg) < self.cols:
					self.w.addstr(cur_line, 0, msg)
					break
				else:
					a = self.last_line_wrapper.wrap(msg)
					self.w.addstr(cur_line, 0, a[0] + CG.MORE_STR)
					if not skip_all:
						if self.notify() == ord('\n'):
							skip_all = True
					msg = " ".join(a[1:])
					cur_line = 0
					self.clear()
		self.msgqueue = ""
