from __future__ import absolute_import, division, print_function, unicode_literals

import textwrap

from config.bindings import Bind
from enums.colors import Pair
from window.base_window import BaseWindow


MORE_STR = " More"
MORE_STR_LEN = len(MORE_STR)


class MessageBar(BaseWindow):

    """Handles the messaging bar system."""

    def __init__(self, *a, **k):
        BaseWindow.__init__(self, *a, **k)

        self.history = []
        self.msgqueue = []
        self.wrap = textwrap.TextWrapper(width=(self.cols - MORE_STR_LEN)).wrap

    def update(self):
        self.clear()
        if self.msgqueue:
            self.print_event(self.msgqueue)
            self.history.append(self.msgqueue)
            self.msgqueue = []
        self.blit()

    def queue_msg(self, *args):
        for obj in args:
            self.msgqueue.append(str(obj))

    def print_event(self, event):
        skip = False
        lines = self.wrap(" ".join(event))
        for i, line in enumerate(lines):
            self.addstr(i % self.rows, 0, line)
            if i % self.rows == self.rows - 1 and i != len(lines) - 1:
                self.addstr(self.rows - 1, self.cols - MORE_STR_LEN, MORE_STR, Pair.Green)
                if self.selective_get_key(Bind.Last_Message + Bind.Cancel, refresh=True) in Bind.Last_Message:
                    skip = True
                    break
                self.clear()
        if skip:
            self.clear()
            for i in range(self.rows):
                self.addstr(i, 0, lines[i - self.rows])

    def print_history(self):
        keep_asking = True
        for i, event in enumerate(self.history):
            self.print_event(["History line {}:".format(i)] + event)
            if keep_asking and self.selective_get_key(Bind.Cancel + Bind.Last_Message, refresh=True) in Bind.Last_Message:
                keep_asking = False
