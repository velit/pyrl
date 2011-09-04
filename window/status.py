import curses
from window.window import Window


class StatusBar(Window):
	"""Handles the status bar system."""

	def __init__(self, window):
		super().__init__(window)
		self.lines, self.width = self.w.getmaxyx()
		self.elements = {}
		self.addcount = 0

	def add_element(self, handle, string, value):
		self.elements[handle] = self.addcount, string, value
		self.addcount += 1

	def set_element(self, handle, string, value):
		self.elements[handle] = self.elements[handle][0], string, value

	def del_element(self, handle):
		del self.elements[handle]

	def update(self):
		self.clear()
		self.print_elements()
		Window.update(self)

	def print_elements(self):
		for priority, string, value in sorted(self.elements.values()):
			self.w.addstr(string + "[" + str(value()) + "] ")
