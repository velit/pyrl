from collections import deque

class TurnScheduler:
	def __init__(self):
		self.queue = deque()

	def add(self, actor):
		self.queue.append(actor)

	def get(self):
		actor = self.queue.popleft()
		self.queue.append(actor)
		return actor

	def remove(self, actor):
		self.queue.remove(actor)

	def get_actor_set(self):
		return set(self.queue)
