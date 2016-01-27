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
    lines_amount = len(lines)
    header_and_footer_size = 4
    visible_amount = min(window.rows - header_and_footer_size, lines_amount)
    return_keys = return_keys + Bind.Cancel
    all_keys = Bind.scroll_keys + select_keys + return_keys

    if select_keys:
        visible_amount = min(len(select_keys), lines_amount)
        select_keys = select_keys[:visible_amount]
        keys_str = tuple(_capitalize_single_chars(select_keys))

    view_offset = 0
    while True:
        print_lines = _slice_lines(lines, view_offset, view_offset + visible_amount)
        if select_keys:
            print_lines = ("{0} - {1}".format(key, line.string) for key, line in zip(keys_str, print_lines))

        _print_view(window, print_lines, header, footer)
        key = window.selective_get_key(all_keys, refresh=True)

        if key in return_keys:
            return key
        elif key in select_keys:
            return lines[select_keys.index(key) + view_offset].return_value
        elif key in Bind.scroll_keys:
            view_offset = _new_offset(view_offset, key, visible_amount, lines_amount)
        else:
            assert False, "Got unhandled key as input {}".format(key)


_multi = "{}/{} to scroll  {}/{} for next/previous line  {}/{} to (de)select all  {} to close"
_multi = _multi.format(Bind.Next_Page.key, Bind.Previous_Page.key,
                       Bind.Next_Line.key, Bind.Previous_Line.key,
                       Bind.Deselect_All.key, Bind.Select_All.key, Bind.Cancel.key)


def multi_select_lines_view(window, lines, select_keys, return_keys=(), header="", footer=_multi):
    """
    Render a view based on parameter lines which is a sequence of Line namedtuples.

    Can select multiple lines. Returns a (return_key, retvals_of_selected_lines) tuple.
    """
    if not select_keys:
        raise ValueError("LinesView initialization has to have non-empty select"
                            "_keys when using multi select mode")

    lines_amount = len(lines)
    header_and_footer_size = 4
    visible_amount = min(window.rows - header_and_footer_size, lines_amount, len(select_keys))
    select_keys = select_keys[:visible_amount]
    return_keys = return_keys + Bind.Cancel
    all_keys = Bind.scroll_keys + select_keys + return_keys + Bind.Select_All + Bind.Deselect_All
    keys_str = tuple(_capitalize_single_chars(select_keys))

    view_offset = 0
    selected_indexes = set()
    while True:
        print_lines = _slice_lines(lines, view_offset, view_offset + visible_amount)
        print_lines = tuple("{} {} {}".format(key, _selection_symbol(selected_indexes, view_offset + i), line.string)
                        for i, (key, line) in enumerate(zip(keys_str, print_lines)))

        _print_view(window, print_lines, header, footer)

        key = window.selective_get_key(all_keys, refresh=True)

        if key in return_keys:
            return key, tuple(lines[i].return_value for i in sorted(selected_indexes))
        elif key in select_keys:
            selected_indexes ^= {select_keys.index(key) + view_offset}
        elif key in Bind.scroll_keys:
            view_offset = _new_offset(view_offset, key, visible_amount, lines_amount)
        elif key in Bind.Select_All:
            selected_indexes = set(range(lines_amount))
        elif key in Bind.Deselect_All:
            selected_indexes.clear()
        else:
            assert False, "Got unhandled key as input {}".format(key)


def _selection_symbol(selected, index):
    return "+" if index in selected else "-"


def _capitalize_single_chars(seq):
    for key in seq:
        if len(key) == 1:
            yield key.upper()
        else:
            yield key


def _print_view(window, print_lines, header="", footer="", main_view_pos=2, header_pos=0, footer_pos=-1):
    window.clear()
    if header is not None:
        window.draw_banner(header, y_offset=header_pos)
    window.draw_lines(print_lines, y_offset=main_view_pos)
    if footer is not None:
        window.draw_banner(footer, y_offset=footer_pos)


def _slice_lines(seq, start_index=0, stop_index=None):
    if stop_index is not None:
        for i in range(start_index, stop_index):
            yield seq[i]
    else:
        for i in range(start_index, len(seq)):
            yield seq[i]


def _new_offset(offset, key, visible_amount, lines_amount):
    if key in Bind.Next_Line:
        offset += 1
    elif key in Bind.Next_Page:
        offset += visible_amount - 1
    elif key in Bind.Previous_Line:
        offset -= 1
    elif key in Bind.Previous_Page:
        offset -= visible_amount - 1
    max_offset = max(0, lines_amount - visible_amount)
    offset = min(max(0, offset), max_offset)
    return offset
