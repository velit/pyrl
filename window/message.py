import textwrap
from .pyrl_window import PyrlWindow


MORE_STR = " (more)"


class MessageBar(PyrlWindow):
	"""Handles the messaging bar system."""

	def __init__(self, concrete_window):
		PyrlWindow.__init__(self, concrete_window)

		self.msgqueue = ""

		#accommodate for printing the newline character
		self.wrapper = textwrap.TextWrapper(width=(self.cols))

		#accommodate for the more_str if the messages continue on the next page
		self.last_line_wrapper = textwrap.TextWrapper(width=(self.cols - len(MORE_STR) - 1))

	def prepare_flush(self):
		self.print_queue()
		PyrlWindow.prepare_flush(self)

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
					self.mvaddstr(cur_line, 0, msg)
					break
				else:
					a = self.wrapper.wrap(msg)
					self.w.mvaddstr(cur_line, 0, a[0])
					msg = " ".join(a[1:])
					cur_line += 1
			elif cur_line == self.rows - 1:
				if len(msg) < self.cols:
					self.w.addstr(cur_line, 0, msg)
					break
				else:
					a = self.last_line_wrapper.wrap(msg)
					self.w.addstr(cur_line, 0, a[0] + MORE_STR)
					if not skip_all:
						if self.notify() == ord('\n'):
							skip_all = True
					msg = " ".join(a[1:])
					cur_line = 0
					self.clear()
		self.msgqueue = ""
