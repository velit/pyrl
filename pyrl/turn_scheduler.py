from __future__ import annotations

import heapq
from collections import deque

class PollingTurnScheduler:
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

class TurnScheduler:

    """Priority queue based turn scheduler. Behaves in LIFO fashion with equal time values."""

    def __init__(self):
        self.pq = []
        self.time = 0
        self.remove_set = set()
        # count is used to resolve time collisions in the queue
        self.count = 0

    def addpop(self, event, time_delta):
        self.count -= 1
        entry = (self.time + time_delta, self.count, event)
        event_time, count, event = heapq.heappushpop(self.pq, entry)
        return event, event_time - self.time

    def add(self, event, time_delta):
        self.count -= 1
        entry = (self.time + time_delta, self.count, event)
        heapq.heappush(self.pq, entry)

    def remove(self, event):
        self.remove_set.add(event)
        self._clean_removed_events()

    def _clean_removed_events(self):
        while self.pq and self.pq[0][2] in self.remove_set:
            time, count, event = heapq.heappop(self.pq)
            self.remove_set.remove(event)

    def advance_time(self):
        self._clean_removed_events()
        event_time, count, event = self.pq[0]
        time_delta = event_time - self.time
        self.time = event_time
        return event, time_delta
