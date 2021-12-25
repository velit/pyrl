from __future__ import annotations

class Event:

    def __init__(self):
        self.observers = []

    def subscribe(self, function):
        self.observers.append(function)

    def unsubscribe(self, function):
        self.observers.remove(function)

    def trigger(self, *args, **kwargs):
        for observer in self.observers:
            observer(*args, **kwargs)
