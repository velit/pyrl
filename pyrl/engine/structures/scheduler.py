from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar('T')
Entry = tuple[int, int, T]

@dataclass(eq=False)
class Scheduler(Generic[T]):
    """Priority queue based scheduler. Behaves in LIFO fashion with equal time values."""

    priority_queue: list[tuple[int, int, T]] = field(default_factory=list, repr=False)
    remove_set: set[tuple[int, int, T]] = field(default_factory=set, repr=False)
    time: int = 0
    count: int = 0  # count is used to resolve time collisions in the queue

    def add(self, item: T, time_delta: int) -> None:
        self.count -= 1
        entry = (self.time + time_delta, self.count, item)
        heapq.heappush(self.priority_queue, entry)

    def pop(self) -> tuple[T, int]:
        """Pops the next item and its time delta."""
        self._clean_queue_front()
        item_time, count, item = heapq.heappop(self.priority_queue)
        time_delta = item_time - self.time
        self.time = item_time
        return item, time_delta

    def remove(self, remove_item: T) -> None:
        self.remove_set |= {(time, count, item) for time, count, item in self.priority_queue if item == remove_item}
        self._clean_queue_front()

    def _clean_queue_front(self) -> None:
        """Remove marked items from the front of the queue"""
        while self.priority_queue and self.priority_queue[0] in self.remove_set:
            self.remove_set.remove(heapq.heappop(self.priority_queue))
