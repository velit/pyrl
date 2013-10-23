from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import textwrap

from window.base_window import BaseWindow


class StatusBar(BaseWindow):
    """Handles the status bar system."""

    def __init__(self, *a, **k):
        BaseWindow.__init__(self, *a, **k)

        self.elements = []
        self.wrapper = textwrap.TextWrapper(width=self.cols)

    def update(self):
        self.clear()
        self.print_elements()
        self.blit()

    def add_element(self, string, getter):
        self.elements.append((string, getter))

    def print_elements(self):
        status_string = "  ".join("{}:{}".format(string, getter()) for string, getter in self.elements)
        lines = self.wrapper.wrap(status_string)
        for i, line in enumerate(lines):
            self.addstr(i, 0, line)
