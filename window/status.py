import textwrap
from functools import wraps

from window.base_window import BaseWindow


class StatusBar(BaseWindow):

    """Handles the status bar system."""

    @wraps(BaseWindow.__init__, assigned=())
    def __init__(self, *args, **kwargs):
        BaseWindow.__init__(self, *args, **kwargs)

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
            self.draw_str(line, (i, 0))
