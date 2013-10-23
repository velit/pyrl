from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import deque


class TurnScheduler(object):
    _TURN_DELIMITER = "Turn delimiter"

    def __init__(self):
        self.queue = deque()
        self.queue.append(self._TURN_DELIMITER)

    def add(self, actor):
        self.queue.append(actor)

    def get_actor_and_is_newcycle(self):
        newcycle = False
        if self.queue[0] == self._TURN_DELIMITER:
            self.queue.rotate(-1)
            newcycle = True

        self.queue.append(self.queue[0])
        return self.queue.popleft(), newcycle

    def remove(self, actor):
        self.queue.remove(actor)
