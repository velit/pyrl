from __future__ import absolute_import, division, print_function, unicode_literals

import textwrap
import logging

import io_wrappers.mock
from bindings import Bind
from enums.colors import Pair
from window.base_window import BaseWindow
from functools import wraps


MORE_STR = " More"
MORE_STR_LEN = len(MORE_STR)


class MessageBar(BaseWindow):

    """Handles the messaging bar system."""

    @wraps(BaseWindow.__init__, assigned=())
    def __init__(self, *args, **kwargs):
        BaseWindow.__init__(self, *args, **kwargs)

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
        if self.cursor_win.implementation == io_wrappers.mock.IMPLEMENTATION:
            for obj in args:
                logging.debug("io.msg: {}".format(obj))
        else:
            for obj in args:
                self.msgqueue.append(str(obj))

    def print_event(self, event):
        skip = False
        lines = self.wrap(" ".join(event))
        for i, line in enumerate(lines):
            self.draw_str(line, (i % self.rows, 0))
            if i % self.rows == self.rows - 1 and i != len(lines) - 1:
                self.draw_str(MORE_STR, (self.rows - 1, self.cols - MORE_STR_LEN), Pair.Green)
                if self.selective_get_key(Bind.Last_Message + Bind.Cancel, refresh=True) in Bind.Last_Message:
                    skip = True
                    break
                self.clear()
        if skip:
            self.clear()
            for i in range(self.rows):
                self.draw_str(lines[i - self.rows], (i, 0))

    def print_history(self):
        keep_asking = True
        for i, event in enumerate(self.history):
            self.print_event(["History line {}:".format(i)] + event)
            if keep_asking and self.selective_get_key(Bind.Cancel + Bind.Last_Message, refresh=True) in Bind.Last_Message:
                keep_asking = False
