from __future__ import absolute_import, division, print_function, unicode_literals

from heapq import heappush, heappop
from collections import deque


class PollingTurnScheduler(object):
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


class TurnScheduler(object):

    """Priority queue based turn scheduler. Behaves in LIFO fashion with equal time values."""

    def __init__(self):
        self.priority_queue = []
        self.time = 0
        self.remove_set = set()
        # count is used to resolve time collisions in the queue
        self.count = 0

    def add(self, event, time_delta):
        self.count -= 1
        entry = (self.time + time_delta, self.count, event)
        heappush(self.priority_queue, entry)

    def remove(self, event):
        self.remove_set.add(event)

    def _clean_removed_events(self):
        while self.priority_queue[0][2] in self.remove_set:
            time, count, event = heappop(self.priority_queue)
            self.remove_set.remove(event)

    def advance_time(self):
        self._clean_removed_events()
        new_time, count, event = heappop(self.priority_queue)
        time_delta = new_time - self.time
        self.time = new_time
        return event, time_delta
