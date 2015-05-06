from __future__ import absolute_import, division, print_function, unicode_literals
from config.bindings import Bind


def lines_view(base_window, lines, header="", use_selectable_lines=False):
    """
    Render a view using lines == a sequence of strings.

    If use_selectable_lines and user selects line: return index of selected line.
    """
    view = LinesView(base_window, lines, header, use_selectable_lines)
    return view.render()


class LinesView(object):

    header_pos = 0
    main_view_pos = 2
    footer_pos = -1
    view_overhead = 4

    footer_fmt = "{}/{} to scroll  {}/{} for next/previous line  {} to close"
    footer = footer_fmt.format(Bind.Next_Page.key, Bind.Previous_Page.key,
                               Bind.Next_Line.key, Bind.Previous_Line.key, Bind.Cancel.key)

    def __init__(self, window, lines, header, use_selectable_lines):
        self.window = window
        self.lines = lines
        self.header = header

        self.index = 0
        self.key_seq = Bind.Cancel + Bind.scroll_keys
        if use_selectable_lines:
            self.select_keys = Bind.Item_Select_Keys
            self.fmt = "{0} - {1}"
            self.key_seq += self.select_keys
        else:
            self.select_keys = range(self.window.rows - self.view_overhead)
            self.fmt = "{1}"

    def render(self):
        while True:
            keys_lines = zip(self.select_keys, self._iter_slice(self.lines, self.index))
            print_lines = (self.fmt.format(*line) for line in keys_lines)
            self._print_view(print_lines)

            key = self.window.selective_get_key(self.key_seq, refresh=True)

            if key in Bind.Cancel:
                return None
            elif key in Bind.scroll_keys:
                self._update_index(key)
            elif key in self.select_keys:
                return self.select_keys.index(key) + self.index

    def _print_view(self, print_lines):
        self.window.clear()
        self.window.draw_banner(self.header, y_offset=self.header_pos)
        self.window.draw_lines(print_lines, y_offset=self.main_view_pos)
        self.window.draw_banner(self.footer, y_offset=self.footer_pos)

    def _iter_slice(self, seq, start_index=0):
        for i in range(start_index, len(seq)):
            yield seq[i]

    def _update_index(self, key):
        i = self.index
        if key in Bind.Next_Line:
            i += 1
        elif key in Bind.Next_Page:
            i += len(self.select_keys) - 1
        elif key in Bind.Previous_Line:
            i -= 1
        elif key in Bind.Previous_Page:
            i -= len(self.select_keys) - 1
        min_i, max_i = 0, max(0, len(self.lines) - len(self.select_keys))
        i = min(max(i, min_i), max_i)
        self.index = i
