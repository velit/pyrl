import menu
import menu_h
import const.game as GAME


class PyrlWindow:

	def __init__(self, concrete_window):
		self._concrete_window = concrete_window

	def __getattr__(self, name):
		return getattr(self._concrete_window, name)

	def notify(self, print_str=None):
		return self.sel_getch(print_str, char_list=GAME.DEFAULT)

	def sel_getch(self, print_str=None, char_list=GAME.ALL):
		if print_str is not None:
			self.clear()
			self.addstr(print_str)
		c = self.getch()
		while c not in char_list:
			c = self.getch()
		return c

	def wrap_print(self, words):
		self.clear()
		str = words
		cur_line = 0
		skip_all = False
		while True:
			if cur_line < self.lines - 1:
				if len(str) < self.width:
					self.addstr(cur_line, 0, str)
					break
				else:
					a = self.wrapper.wrap(str)
					self.addstr(cur_line, 0, a[0])
					str = " ".join(a[1:])
					cur_line += 1
			elif cur_line == self.lines - 1:
				if len(str) < self.width:
					self.addstr(cur_line, 0, str)
					break
				else:
					a = self.last_line_wrapper.wrap(str)
					self.addstr(cur_line, 0, a[0] + self.more_str)
					if not skip_all:
						c = self.getch_from_list(list=(ord('\n'), ord(' ')))
						if c == ord('\n'):
							skip_all = True
					str = " ".join(a[1:])
					cur_line = 0
					self.clear()
		self.msgqueue = ""

	def draw_menu(self, *a, **k):
		return menu.draw(self, *a, **k)

	def draw_h_menu(self, *a, **k):
		return menu_h.draw(self, *a, **k)
