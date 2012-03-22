import textwrap
import const.keys as KEY
from const.colors import GREEN
from window.base_window import BaseWindow


MORE_STR_LEN = 2

class MessageBar(BaseWindow):
	"""Handles the messaging bar system."""

	def __init__(self, *a, **k):
		BaseWindow.__init__(self, *a, **k)

		self.history = []
		self.msgqueue = []
		self.wrap = textwrap.TextWrapper(width=(self.cols - MORE_STR_LEN)).wrap

	def update(self):
		if self.msgqueue:
			self.print_event(self.msgqueue)
			self.history.append(self.msgqueue)
			self.msgqueue = []
		else:
			self.erase()
		self.blit()

	def queue_msg(self, *args):
		for obj in args:
			self.msgqueue.append(str(obj))

	def _selective_getch(self, char_seq=KEY.GROUP_MORE):
		while True:
			c = self.get_key()
			if c in char_seq:
				return c

	def print_event(self, event):
		skip = False
		lines = self.wrap(" ".join(event))
		self.erase()
		for i, line in enumerate(lines):
			self.addstr(i % self.rows, 0, line)
			if i % self.rows == self.rows - 1 and i != len(lines) - 1:
				self.addch(self.rows - 1, self.cols - 1, ("M", GREEN))
				self.refresh()
				if self._selective_getch() == KEY.ENTER:
					skip = True
					break
				self.erase()
		if skip:
			self.erase()
			for i in range(self.rows):
				self.addstr(i, 0, lines[i - self.rows])

	def print_history(self):
		for i, event in enumerate(self.history):
			self.print_event(["History line {}:".format(i)] + event)
			self._selective_getch()
