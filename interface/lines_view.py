from __future__ import absolute_import, division, print_function, unicode_literals

from config.bindings import Bind


def lines_view(*keys, **args):
    """
    Render a view using lines as sequence of strings.

    If select_keys is defined and user presses key, return index of the appropriate line.
    """
    view = LinesView(*keys, **args)
    return view.render()


class LinesView(object):

    header_pos = 0
    main_view_pos = 2
    footer_pos = -1
    view_overhead = 4

    footer_fmt = "{}/{} to scroll  {}/{} for next/previous line  {} to close"
    footer = footer_fmt.format(Bind.Next_Page.key, Bind.Previous_Page.key,
                               Bind.Next_Line.key, Bind.Previous_Line.key, Bind.Cancel.key)

    def __init__(self, window, lines, select_keys=(), return_keys=(), header="", footer=None):
        self.window = window
        self.lines = tuple(lines)
        self.header = header
        if footer is not None:
            self.footer = footer

        self.index = 0
        self.view_lines = self.window.rows - self.view_overhead
        self.select_keys = select_keys
        self.return_keys = return_keys

        if self.select_keys:
            self.select_keys = select_keys[:self.view_lines]
            self.visible_amount = min(len(self.select_keys), len(self.lines))
            upper_one_char = lambda key: key.upper() if len(key) == 1 else key
            self.select_keys_str = tuple(upper_one_char(key) for key in self.select_keys)
        else:
            self.visible_amount = min(self.view_lines, len(self.lines))

        self.key_seq = Bind.Cancel + Bind.scroll_keys + self.select_keys + self.return_keys

    def render(self):
        while True:
            if self.select_keys:
                lines = self._iter_slice(self.lines, self.index, self.index + self.visible_amount)
                keys_lines = zip(self.select_keys_str, lines)
                print_lines = ("{0} - {1}".format(key, line) for key, line in keys_lines)
            else:
                print_lines = self._iter_slice(self.lines, self.index, self.index + self.visible_amount)

            self._print_view(print_lines)

            key = self.window.selective_get_key(self.key_seq, refresh=True)

            if key in self.return_keys:
                return key
            elif key in Bind.Cancel:
                return None
            elif key in Bind.scroll_keys:
                self._update_index(key)
            elif key in self.select_keys:
                return self.select_keys.index(key) + self.index
            else:
                assert False, "Got unhandled key as input {}".format(key)

    def _print_view(self, print_lines):
        self.window.clear()
        self.window.draw_banner(self.header, y_offset=self.header_pos)
        self.window.draw_lines(print_lines, y_offset=self.main_view_pos)
        self.window.draw_banner(self.footer, y_offset=self.footer_pos)

    def _iter_slice(self, seq, start_index=0, stop_index=None):
        if stop_index is not None:
            for i in range(start_index, stop_index):
                yield seq[i]
        else:
            for i in range(start_index, len(seq)):
                yield seq[i]

    def _update_index(self, key):
        i = self.index
        if key in Bind.Next_Line:
            i += 1
        elif key in Bind.Next_Page:
            i += self.visible_amount - 1
        elif key in Bind.Previous_Line:
            i -= 1
        elif key in Bind.Previous_Page:
            i -= self.visible_amount - 1
        min_i, max_i = 0, max(0, len(self.lines) - self.visible_amount)
        i = min(max(i, min_i), max_i)
        self.index = i
