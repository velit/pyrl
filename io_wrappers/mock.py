from __future__ import absolute_import, division, print_function, unicode_literals

from collections import deque


class MockInputEnd(Exception):
    pass


class MockWrapper():

    _prepared_input = deque()

    def __init__(self):
        pass

    @classmethod
    def _prepare_input(cls, input_seq):
        cls._prepared_input.extend(input_seq)

    @staticmethod
    def flush():
        pass

    @staticmethod
    def suspend():
        pass

    @staticmethod
    def resume():
        pass

    @classmethod
    def new_window(cls, size):
        return cls()

    def get_key(self):
        try:
            return self._prepared_input.popleft()
        except IndexError:
            raise MockInputEnd()

    def check_key(self):
        try:
            return self._prepare_input.popleft()
        except IndexError:
            raise MockInputEnd()

    def clear(self):
        pass

    def blit(self, size, screen_position):
        pass

    def get_dimensions(self):
        pass

    def addch(self, y, x, char):
        pass

    def addstr(self, y, x, string, color=None):
        pass

    def draw(self, char_payload_sequence):
        pass

    def draw_reverse(self, char_payload_sequence):
        pass