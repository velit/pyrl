from .pyrl_window import PyrlWindow


class StatusBar(PyrlWindow):
	"""Handles the status bar system."""

	def __init__(self, concrete_window):
		super().__init__(concrete_window)

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
		self._concrete_window.update()

	def print_elements(self):
		for priority, string, value in sorted(self.elements.values()):
			self.w.addstr(string + "[" + str(value()) + "] ")
