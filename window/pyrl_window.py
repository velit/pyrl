import menu
import menu_h
import const.game as GAME


class PyrlWindow(object):

	def __init__(self, concrete_window):
		self._w = concrete_window
		self.rows, self.cols = self.get_dimensions()


	# Proxy functions

	def addch(self, y, x, char):
		self._w.addch(y, x, char)

	def addstr(self, y, x, string, color=None):
		self._w.addstr(y, x, string, color)

	def getch(self):
		return self._w.getch()

	def get_dimensions(self):
		return self._w.get_dimensions()

	def clear(self):
		self._w.clear()

	def prepare_flush(self):
		self._w.prepare_flush()

	def flush(self):
		self._w.flush()


	# PyrlWindow added functions

	def notify(self, print_str=None):
		return self.sel_getch(print_str, char_list=GAME.DEFAULT)

	def sel_getch(self, print_str=None, char_list=GAME.ALL):
		if print_str is not None:
			self.clear()
			self.mvaddstr(0, 0, print_str)
		c = self.getch()
		while c not in char_list:
			c = self.getch()
		return c

	def draw_menu(self, *a, **k):
		return menu.draw(self, *a, **k)

	def draw_h_menu(self, *a, **k):
		return menu_h.draw(self, *a, **k)
