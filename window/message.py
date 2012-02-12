import textwrap
import const.keys as KEY
from .pyrl_window import PyrlWindow
from const.colors import GREEN


MORE_STR_LEN = 2

class MessageBar(PyrlWindow):
	"""Handles the messaging bar system."""

	def __init__(self, *a, **k):
		PyrlWindow.__init__(self, *a, **k)

		self.msgqueue = []
		self.wrap = textwrap.TextWrapper(width=(self.cols - MORE_STR_LEN)).wrap

	def prepare_flush(self):
		self.clear()
		self.print_queue()
		self.msgqueue = []
		PyrlWindow.prepare_flush(self)

	def queue_msg(self, *args):
		for obj in args:
			self.msgqueue.append(str(obj))

	def _selective_getch(self, char_seq):
		while True:
			c = self.getch()
			if c in char_seq:
				return c

	def print_queue(self):
		skip = False
		lines = self.wrap(" ".join(self.msgqueue))

		for i, line in enumerate(lines):
			self.addstr(i % self.rows, 0, line)

			if i % self.rows == self.rows - 1 and i != len(lines) - 1:
				self.addch(self.rows - 1, self.cols - 1, ("M", GREEN))

				self.refresh()
				if self._selective_getch(KEY.GROUP_DEFAULT) in "\n\r":
					skip = True
					break

				self.clear()

		if skip:
			self.clear()
			for i in range(self.rows):
				self.addstr(i, 0, lines[i - self.rows])
