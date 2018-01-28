import logging
from collections import deque

from pyrl.enums.keys import Key


IMPLEMENTATION = "mock"


class MockInputEnd(Exception):
    pass


class MockWrapper(object):

    implementation = IMPLEMENTATION

    def __init__(self):
        self._prepared_input = deque()

    def _prepare_input(self, input_seq):
        self._prepared_input.extend(input_seq)

    def flush(self):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass

    def new_window(self, dimensions):
        return MockWrapperWindow(self)


class MockWrapperWindow(object):

    implementation = IMPLEMENTATION

    def __init__(self, wrapper):
        self.wrapper = wrapper

    def get_key(self):
        try:
            key = self.wrapper._prepared_input.popleft()
            logging.debug("Returning key {}".format(key))
            return key
        except IndexError:
            raise MockInputEnd()

    def check_key(self):
        return Key.NO_INPUT

    def clear(self):
        pass

    def blit(self, size, screen_position):
        pass

    def get_dimensions(self):
        pass

    def draw_char(self, coord, char):
        pass

    def draw_str(self, coord, string, color=None):
        pass

    def draw(self, char_payload_sequence):
        pass

    def draw_reverse(self, char_payload_sequence):
        pass
