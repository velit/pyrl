import textwrap
import const.keys as KEY
from .pyrl_window import PyrlWindow
from const.colors import GREEN


MORE_STR_LEN = 2

class MessageBar(PyrlWindow):
	"""Handles the messaging bar system."""

	def __init__(self, *a, **k):
		PyrlWindow.__init__(self, *a, **k)

		self.history = []
		self.msgqueue = []
		self.wrap = textwrap.TextWrapper(width=(self.cols - MORE_STR_LEN)).wrap

	def update(self):
		if self.msgqueue:
			self.print_event(self.msgqueue)
			self.history.append(self.msgqueue)
			self.msgqueue = []
		else:
			self.clear()
		self.blit()

	def queue_msg(self, *args):
		for obj in args:
			self.msgqueue.append(str(obj))

	def _selective_getch(self, char_seq=KEY.GROUP_DEFAULT):
		while True:
			c = self.getch()
			if c in char_seq:
				return c

	def print_event(self, event):
		skip = False
		lines = self.wrap(" ".join(event))
		self.clear()
		for i, line in enumerate(lines):
			self.addstr(i % self.rows, 0, line)
			if i % self.rows == self.rows - 1 and i != len(lines) - 1:
				self.addch(self.rows - 1, self.cols - 1, ("M", GREEN))
				self.refresh()
				if self._selective_getch() == KEY.ENTER:
					skip = True
					break
				self.clear()
		if skip:
			self.clear()
			for i in range(self.rows):
				self.addstr(i, 0, lines[i - self.rows])

	def print_history(self):
		for i, event in enumerate(self.history):
			self.print_event(["History line {}:".format(i)] + event)
			self._selective_getch()
