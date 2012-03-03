class PyrlWindow(object):

	def __init__(self, cursor_lib, concrete_handle, blit_args=None):
		self.cursor_lib = cursor_lib
		self.h = concrete_handle
		self.rows, self.cols = self.get_dimensions()
		self.cursor_lib.init_handle(self.h)
		self.blit_args = blit_args

	def addch(self, y, x, char):
		self.cursor_lib.addch(self.h, y, x, char)

	def addstr(self, y, x, string, color=None):
		self.cursor_lib.addstr(self.h, y, x, string, color)

	def draw(self, char_payload_sequence):
		self.cursor_lib.draw(self.h, char_payload_sequence)

	def draw_reverse(self, char_payload_sequence):
		self.cursor_lib.draw_reverse(self.h, char_payload_sequence)
		for y, x, (symbol, color) in char_payload_sequence:
			self.addch(y, x, (symbol, color[::-1]))

	def clear(self):
		self.cursor_lib.clear(self.h)

	def getch(self):
		return self.cursor_lib.getch(self.h)

	def get_dimensions(self):
		return self.cursor_lib.get_dimensions(self.h)

	def blit(self):
		self.cursor_lib.blit(self.h, self.blit_args)

	def flush(self):
		self.cursor_lib.flush()

	def refresh(self):
		self.blit()
		self.flush()

	def sub_handle(self, rows, cols, offset_y, offset_x):
		new_handle, blit_args = self.cursor_lib.subwindow_handle(self.h, rows, cols, offset_y, offset_x)
		return new_handle, blit_args

	def suspend(self):
		self.cursor_lib.suspend(self.h)
