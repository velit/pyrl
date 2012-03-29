import textwrap
from window.base_window import BaseWindow


class StatusBar(BaseWindow):
	"""Handles the status bar system."""

	def __init__(self, *a, **k):
		BaseWindow.__init__(self, *a, **k)

		self.elements = []
		self.modified = False
		self.wrapper = textwrap.TextWrapper(width=self.cols)

	def update(self):
		if self.modified:
			self.elements.sort()
			self.modified = False
		self.clear()
		self.print_elements()
		self.blit()

	def add_element(self, string, getter):
		self.elements.append((string, getter))
		self.modified = True

	def print_elements(self):
		status_string = "  ".join("{}:{}".format(string, getter()) for string, getter in self.elements)
		lines = self.wrapper.wrap(status_string)
		for i, line in enumerate(lines):
			self.addstr(i, 0, line)
