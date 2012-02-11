import textwrap
from .pyrl_window import PyrlWindow


class StatusBar(PyrlWindow):
	u"""Handles the status bar system."""

	def __init__(self, concrete_window):
		PyrlWindow.__init__(self, concrete_window)

		self.elements = []
		self.wrapper = textwrap.TextWrapper(width=self.cols)

	def add_element(self, handle, string, getter):
		self.elements.append((string, getter))

	def prepare_flush(self):
		self.elements.sort()
		self.clear()
		self.print_elements()
		PyrlWindow.prepare_flush(self)

	def print_elements(self):
		status_string = " ".join(u"{}[{}]".format(string, unicode(getter())) for string, getter in self.elements)
		lines = self.wrapper.wrap(status_string)
		for i, line in enumerate(lines):
			self.addstr(i, 0, line)
