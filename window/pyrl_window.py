

class PyrlWindow(object):

	def __init__(self, cursor_lib, concrete_handle, blit_args=None):
		self.cursor_lib = cursor_lib
		self.handle = concrete_handle
		self.rows, self.cols = self.get_dimensions()
		self.cursor_lib.init_handle(self.handle)
		self.blit_args = blit_args

	# Proxy functions
	def addch(self, y, x, char):
		self.cursor_lib.addch(self.handle, y, x, char)

	def addstr(self, y, x, string, color=None):
		self.cursor_lib.addstr(self.handle, y, x, string, color)

	def clear(self):
		self.cursor_lib.clear(self.handle)

	def prepare_flush(self):
		if self.blit_args is None:
			self.cursor_lib.prepare_flush(self.handle)
		else:
			self.cursor_lib.blit(self.blit_args)

	def flush(self):
		self.cursor_lib.flush()

	def getch(self):
		return self.cursor_lib.getch(self.handle)

	def get_dimensions(self):
		return self.cursor_lib.get_dimensions(self.handle)

	def SubWindow(self, WindowType, rows, cols, offset_y, offset_x):
		new_handle = self.cursor_lib.subwindow(self.handle, rows, cols, offset_y, offset_x)
		if hasattr(self.cursor_lib, "blit"):
			blit_args = (new_handle, 0, 0, cols, rows, self.handle, offset_x, offset_y, 1.0, 1.0)
		else:
			blit_args = None
		return WindowType(self.cursor_lib, new_handle, blit_args)
