import textwrap
from .pyrl_window import PyrlWindow
from const.colors import GREEN


MORE_STR_LEN = 3

class MessageBar(PyrlWindow):
	"""Handles the messaging bar system."""

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
		self.msgqueue.append(str(obj))

	def print_queue(self):
		skip = False
		lines = self.wrap(" ".join(self.msgqueue))

		for i, line in enumerate(lines):
			self.addstr(i % self.rows, 0, line)

			if i % self.rows == self.rows - 1 and i != len(lines) - 1:
				self.addch(0, self.cols - 2, ("M", GREEN))
				self.addch(0, self.cols - 1, ("O", GREEN))
				self.addch(1, self.cols - 2, ("R", GREEN))
				self.addch(1, self.cols - 1, ("E", GREEN))

				if self.notify() == ord('\n'):
					skip = True
					break

				self.clear()

		if skip:
			self.clear()
			for i in range(self.rows):
				self.addstr(i, 0, lines[i - self.rows])
