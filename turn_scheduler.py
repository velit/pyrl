from collections import deque


class TurnScheduler(object):
    _TURN_DELIMITER = "Turn delimiter"
    def __init__(self):
        self.queue = deque()
        self.queue.append(self._TURN_DELIMITER)

    def add(self, actor):
        self.queue.append(actor)

    def get(self):
        self.queue.append(self.queue[0])
        return self.queue.popleft()

    def remove(self, actor):
        self.queue.remove(actor)

    def is_new_turn(self):
        if self.queue[0] == self._TURN_DELIMITER:
            self.queue.rotate(-1)
            return True
        else:
            return False
