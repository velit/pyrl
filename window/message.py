import textwrap
from .pyrl_window import PyrlWindow


MORE_STR_LEN = 3

class MessageBar(PyrlWindow):
	u"""Handles the messaging bar system."""

	def __init__(self, concrete_window):
		PyrlWindow.__init__(self, concrete_window)

		self.msgqueue = []
		self.wrap = textwrap.TextWrapper(width=(self.cols - MORE_STR_LEN)).wrap

	def prepare_flush(self):
		self.clear()
		self.print_queue()
		self.msgqueue = []
		PyrlWindow.prepare_flush(self)

	def queue_msg(self, obj):
		self.msgqueue.append(unicode(obj))

	def print_queue(self):
		skip = False
		lines = self.wrap(" ".join(self.msgqueue))

		for i, line in enumerate(lines):
			self.addstr(i % self.rows, 0, line)

			if i % self.rows == self.rows - 1 and i != len(lines) - 1:
				self.addch(0, self.cols - 2, (u"M", u"green"))
				self.addch(0, self.cols - 1, (u"O", u"green"))
				self.addch(1, self.cols - 2, (u"R", u"green"))
				self.addch(1, self.cols - 1, (u"E", u"green"))

				if self.notify() == ord(u'\n'):
					skip = True
					break

				self.clear()

		if skip:
			self.clear()
			for i in range(self.rows):
				self.addstr(i, 0, lines[i - self.rows])
