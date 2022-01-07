from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar('T')
Entry = tuple[int, int, T]

@dataclass(eq=False, order=False, slots=True)
class Scheduler(Generic[T]):
    """Priority queue based scheduler. Behaves in LIFO fashion with equal time values."""

    priority_queue: list[tuple[int, int, T]] = field(default_factory=list, repr=False)
    remove_set: set[T] = field(default_factory=set, repr=False)
    time: int = 0
    count: int = 0  # count is used to resolve time collisions in the queue

    def addpop(self, item: T, time_delta: int) -> tuple[T, int]:
        self.count -= 1
        entry = (self.time + time_delta, self.count, item)
        item_time, count, item = heapq.heappushpop(self.priority_queue, entry)
        return item, item_time - self.time

    def add(self, item: T, time_delta: int) -> None:
        self.count -= 1
        entry = (self.time + time_delta, self.count, item)
        heapq.heappush(self.priority_queue, entry)

    def remove(self, item: T) -> None:
        self.remove_set.add(item)
        self._clean_removed_items()

    def _clean_removed_items(self) -> None:
        while self.priority_queue and self.priority_queue[0][2] in self.remove_set:
            time, count, item = heapq.heappop(self.priority_queue)
            self.remove_set.remove(item)

    def advance_time(self) -> tuple[T, int]:
        self._clean_removed_items()
        item_time, count, item = self.priority_queue[0]
        time_delta = item_time - self.time
        self.time = item_time
        return item, time_delta
