import curses
from window import Window

class StatusBar(Window):
	"""Handles the status bar system."""
	def __init__(self, window, io):
		Window.__init__(self, window)
		self.io = io
		self.lines, self.width = self.w.getmaxyx()
		self.elements = []

	def register(self, string, value):
		self.elements.append((string, value))

	def update(self):
		self.clear()
		self.print_elements()
		Window.update(self)

	def print_elements(self):
		for name, value in self.elements:
			self.w.addstr(name + str(value()) + " ")
