from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import textwrap
import const.keys as KEY
import mappings as MAPPING

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
                self.addch(self.rows - 1, self.cols - 1, ("M", GREEN))
                if self.selective_get_key(MAPPING.GROUP_MORE, refresh=True) == KEY.ENTER:
                    skip = True
                    break
                self.clear()
        if skip:
            self.clear()
            for i in range(self.rows):
                self.addstr(i, 0, lines[i - self.rows])

    def print_history(self):
        for i, event in enumerate(self.history):
            self.print_event(["History line {}:".format(i)] + event)
            self.selective_get_key(MAPPING.GROUP_MORE)
