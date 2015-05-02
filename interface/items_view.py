from __future__ import absolute_import, division, print_function, unicode_literals
from config.mappings import Mapping


def items_view(items, base_window, header="", footer="", selectable_items=False):
    """ Render a view based on str(item) in items."""
    view = ItemsView(base_window)
    return view.render(items, header, footer, selectable_items)


class ItemsView(object):

    header_pos = 0
    main_view_pos = 2
    footer_pos = -1

    def __init__(self, window):
        self.window = window

    def render(self, items, header="", footer="", selectable_items=True):
        items = tuple(items)
        keys = Mapping.Inventory_Keys
        items_len = len(items)
        keys_len = len(keys)

        str_items = tuple(str(item) for item in items)
        key_set = Mapping.Group_Default | Mapping.Scroll_View_Group
        if selectable_items:
            key_set |= set(Mapping.Inventory_Keys)

        i = 0
        while True:
            if selectable_items:
                fmt_str = "{0} - {1}"
            else:
                fmt_str = "- {1}"
            print_lines = (fmt_str.format(*line) for line in zip(keys, self._iter_slice(str_items, i)))
            self.print_view(header, print_lines, footer)

            key = self.window.selective_get_key(key_set, refresh=True)

            if key in Mapping.Group_Default:
                return None
            elif key in keys:
                return items[keys.index(key) + i]
            elif key == Mapping.Next_Line:
                i += 1
            elif key == Mapping.Previous_Line:
                i -= 1
            elif key == Mapping.Next_Page:
                i += keys_len - 1
            elif key == Mapping.Previous_Page:
                i -= keys_len - 1
            i = self._apply_limits(i, items_len, keys_len)

    def print_view(self, header, lines, footer):
        self.window.clear()
        self.window.draw_banner(header, y_offset=self.header_pos)
        self.window.draw_lines(lines, y_offset=self.main_view_pos)
        self.window.draw_banner(footer, y_offset=self.footer_pos)

    def _iter_slice(self, lst, start_index=0):
        for i in range(start_index, len(lst)):
            yield lst[i]

    def _apply_limits(self, index, items_len, selection_keys_len):
        min_i = 0
        max_i = max(0, items_len - selection_keys_len)
        if index < min_i:
            index = min_i
        elif index > max_i:
            index = max_i
        return index
