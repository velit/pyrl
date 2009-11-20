import curses

class StatusBar:
	"""Handles the status bar system."""
	def __init__(self, window, io):
		self.w = window
		self.w.keypad(1)
		self.io = io
		self.lines, self.width = self.w.getmaxyx()
		self.elements = {}

	def register(self, handle, string, value ):
		self.elements[handle] = (string, value)

	def update(self):
		self.w.move(0,0)
		for handle, (name, value) in self.elements.iteritems():
			self.w.addstr(name + str(value())+" ")
		self.w.noutrefresh()
