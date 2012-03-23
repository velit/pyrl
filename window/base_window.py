import time
import const.keys as KEY
import const.game as GAME
from main import cursor_lib


class BaseWindow(object):

	def __init__(self, concrete_handle, blit_args=None):
		self.h = concrete_handle
		self.rows, self.cols = self.get_dimensions()
		cursor_lib.init_handle(self.h)
		self.blit_args = blit_args

	def addch(self, y, x, char):
		cursor_lib.addch(self.h, y, x, char)

	def addstr(self, y, x, string, color=None):
		cursor_lib.addstr(self.h, y, x, string, color)

	def draw(self, char_payload_sequence):
		cursor_lib.draw(self.h, char_payload_sequence)

	def draw_reverse(self, char_payload_sequence):
		cursor_lib.draw_reverse(self.h, char_payload_sequence)

	def add_lines(self, lines):
		for i, line in enumerate(lines):
			self.addstr(i, 0, line)

	def erase(self):
		cursor_lib.erase(self.h)

	# clear is stronger than erase, on ncurses it causes a full refresh
	def clear(self):
		cursor_lib.clear(self.h)

	# Blocking
	def get_key(self, refresh=False):
		if refresh:
			self.refresh()
		return cursor_lib.get_key(self.h)

	# Non-blocking
	def check_key(self, refresh=False):
		if refresh:
			self.refresh()
		return cursor_lib.check_key(self.h)

	# Blocking
	def selective_get_key(self, key_set, refresh=False):
		if refresh:
			self.refresh()
		while True:
			key = self.get_key()
			if key in key_set:
				return key

	# Half-blocking
	def selective_get_key_until_timestamp(self, timestamp, key_set, refresh=False):
		if refresh:
			self.refresh()
		while True:
			if time.time() >= timestamp:
				return KEY.NO_INPUT
			key = self.check_key()
			if key in key_set:
				return key
			time.sleep(GAME.INPUT_INTERVAL)

	def get_dimensions(self):
		return cursor_lib.get_dimensions(self.h)

	def blit(self):
		cursor_lib.blit(self.h, self.blit_args)

	def flush(self):
		cursor_lib.flush()

	def refresh(self):
		self.blit()
		self.flush()

	def redraw(self):
		cursor_lib.redraw(self.h)

	def sub_handle(self, rows, cols, offset_y, offset_x):
		new_handle, blit_args = cursor_lib.subwindow_handle(self.h, rows, cols, offset_y, offset_x)
		return new_handle, blit_args

	def suspend(self):
		cursor_lib.suspend(self.h)
