from __future__ import absolute_import, division, print_function, unicode_literals

from collections import deque


def MockWrapper(prepared_ch_input=None, prepared_str_input=None):

    if prepared_ch_input:
        _MockWrapper._prepare_ch_input(prepared_ch_input)
    if prepared_str_input:
        _MockWrapper._prepare_str_input(prepared_str_input)
    return _MockWrapper


class MockInputEndError(Exception):
    pass


class _MockWrapper():

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

    def get_key(self):
        try:
            return self._prepared_input.popleft()
        except IndexError:
            raise MockInputEndError()

    def check_key(self):
        try:
            return self._prepare_input.popleft()
        except IndexError:
            raise MockInputEndError()

    @classmethod
    def new_window(cls, size):
        return cls()

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
