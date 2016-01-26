from __future__ import absolute_import, division, print_function, unicode_literals

import collections
from config.bindings import Bind


Line = collections.namedtuple("Line", ("return_value", "string"))


_single = "{}/{} to scroll  {}/{} for next/previous line  {} to close"
_single = _single.format(Bind.Next_Page.key, Bind.Previous_Page.key, Bind.Next_Line.key,
                         Bind.Previous_Line.key, Bind.Cancel.key)


def lines_view(window, lines, select_keys=(), return_keys=(), header="", footer=_single):
    """
    Render a view based on parameter lines which is a sequence of Line namedtuples.

    If select_keys is defined and user presses one of them, return the value associated with the line.
    If user presses one of return_keys, return that.
    If user presses one of Bind.Cancel keys return that
    """
    view = LinesView(window, lines, select_keys, return_keys)
    return view.single_select_render(header, footer)


_multi = "{}/{} to scroll  {}/{} for next/previous line  {}/{} to (de)select all  {} to close"
_multi = _multi.format(Bind.Next_Page.key, Bind.Previous_Page.key,
                       Bind.Next_Line.key, Bind.Previous_Line.key,
                       Bind.Deselect_All.key, Bind.Select_All.key, Bind.Cancel.key)


def multi_select_lines_view(window, lines, select_keys=(), return_keys=(), header="", footer=_multi):
    """
    Render a view based on parameter lines which is a sequence of Line namedtuples.

    Can select multiple lines. Returns a (return_key, retvals_of_selected_lines) tuple.
    """
    view = LinesView(window, lines, select_keys, return_keys)
    return view.multi_select_render(header, footer)


class LinesView(object):

    header_pos = 0
    main_view_pos = 2
    footer_pos = -1
    view_overhead = 4

    def __init__(self, window, lines, select_keys=(), return_keys=()):
        self.window = window
        self.lines = tuple(lines)
        self.header = None
        self.footer = None

        self.view_offset = 0
        self.view_height = self.window.rows - self.view_overhead
        self.select_keys = select_keys
        self.selected_line_indexes = set()
        self.return_keys = return_keys + Bind.Cancel

        if self.select_keys:
            self.select_keys = select_keys[:min(self.view_height, len(self.lines))]
            self.visible_amount = min(len(self.select_keys), len(self.lines))
            self.select_keys_str = tuple(self._capitalize_single_chars(self.select_keys))
        else:
            self.visible_amount = min(self.view_height, len(self.lines))

        self.all_keys = Bind.scroll_keys + self.select_keys + self.return_keys

    def single_select_render(self, header="", footer=""):
        self.header = header
        self.footer = footer
        while True:
            if self.select_keys:
                lines = self._iter_slice(self.lines, self.view_offset, self.view_offset + self.visible_amount)
                keys_lines = zip(self.select_keys_str, lines)
                print_lines = ("{0} - {1}".format(key, line.string) for key, line in keys_lines)
            else:
                print_lines = self._iter_slice(self.lines, self.view_offset, self.view_offset + self.visible_amount)

            self._print_view(print_lines)

            key = self.window.selective_get_key(self.all_keys, refresh=True)

            if key in self.return_keys:
                return key
            elif key in self.select_keys:
                return self.lines[self.select_keys.index(key) + self.view_offset].return_value
            elif key in Bind.scroll_keys:
                self._update_index(key)
            else:
                assert False, "Got unhandled key as input {}".format(key)

    def multi_select_render(self, header="", footer=""):

        if not self.select_keys:
            raise ValueError("LinesView initialization has to have non-empty select"
                             "_keys when using multi select mode")

        self.header = header
        self.footer = footer

        while True:

            lines = self._iter_slice(self.lines, self.view_offset, self.view_offset + self.visible_amount)
            keys_lines = zip(self.select_keys_str, lines)
            print_lines = ("{} {} {}".format(key, self._selection_symbol(self.view_offset + i), line.string)
                           for i, (key, line) in enumerate(keys_lines))

            self._print_view(print_lines)

            key = self.window.selective_get_key(self.all_keys, refresh=True)

            if key in self.return_keys:
                return key, tuple(self.lines[i].return_value for i in sorted(self.selected_line_indexes))
            elif key in self.select_keys:
                self._toggle_selection(self.select_keys.index(key) + self.view_offset)
            elif key in Bind.scroll_keys:
                self._update_index(key)
            else:
                assert False, "Got unhandled key as input {}".format(key)

    def _selection_symbol(self, index):
        if index in self.selected_line_indexes:
            return "+"
        else:
            return "-"

    def _toggle_selection(self, index):
        self.selected_line_indexes ^= {index}

    def _capitalize_single_chars(self, seq):
        for key in seq:
            if len(key) == 1:
                yield key.upper()
            else:
                yield key

    def _print_view(self, print_lines):
        self.window.clear()
        if self.header is not None:
            self.window.draw_banner(self.header, y_offset=self.header_pos)
        self.window.draw_lines(print_lines, y_offset=self.main_view_pos)
        if self.footer is not None:
            self.window.draw_banner(self.footer, y_offset=self.footer_pos)

    def _iter_slice(self, seq, start_index=0, stop_index=None):
        if stop_index is not None:
            for i in range(start_index, stop_index):
                yield seq[i]
        else:
            for i in range(start_index, len(seq)):
                yield seq[i]

    def _update_index(self, key):
        i = self.view_offset
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
        self.view_offset = i
