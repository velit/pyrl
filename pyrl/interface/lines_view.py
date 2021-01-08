import collections
import re

from pyrl.binds import Binds

Line = collections.namedtuple("Line", ("display", "return_value"))

def build_lines(iterable):
    return tuple(Line(value, i) for i, value in enumerate(iterable))

_single = "{}/{} scroll  {}/{} next/previous line  {} filter  {} close"
_single = _single.format(Binds.Next_Page.key, Binds.Previous_Page.key, Binds.Next_Line.key,
                         Binds.Previous_Line.key, Binds.Filter, Binds.Cancel.key)
_multi = "{}/{} scroll  {}/{} next/previous line  {}/{} (de)select all  {} filter  {} close"
_multi = _multi.format(Binds.Next_Page.key, Binds.Previous_Page.key,
                       Binds.Next_Line.key, Binds.Previous_Line.key,
                       Binds.Deselect_All.key, Binds.Select_All.key, Binds.Filter, Binds.Cancel.key)

def lines_view(window, lines, multi_select=False, return_keys=Binds.Cancel, select_keys=(),
               header="", footer=None):
    """
    Render a view based on parameter lines which is a sequence of Line namedtuples.

    In normal mode returns (return_key, possible_selected_item), item == None if returned
    by return key.
    In multi_select mode returns (return_key, selected_items)
    """
    if footer is None:
        footer = _multi if multi_select else _single

    orig_lines = tuple(lines)
    orig_select_keys = tuple(select_keys)
    scroll_offset = 0
    selected = set()
    filter_regex = ""
    while True:
        content_size, select_keys, all_keys = _get_vars(window, lines, multi_select,
                                                        orig_select_keys, return_keys)
        print_lines = _get_print_lines(lines, scroll_offset, content_size,
                                       selected, select_keys)
        _print_view(window, print_lines, header + filter_regex, footer)
        key = window.get_key(keys=all_keys, refresh=True)

        if key in Binds.Filter:
            query = "Filter regex (empty to clear): "
            filter_regex = window.get_str(query, (1, 0))
            window.draw_str(" " * (len(query + filter_regex) + 1), (1, 0))
            if filter_regex:
                lines = tuple(line for line in orig_lines if re.search(filter_regex, line.display))
                filter_regex = " (Filter/{})".format(filter_regex)
            else:
                lines = orig_lines
            scroll_offset = 0
        elif key in Binds.ScrollKeys:
            scroll_offset = _new_offset(scroll_offset, key, content_size, len(lines))

        elif multi_select:
            if key in select_keys:
                selected ^= {lines[select_keys.index(key) + scroll_offset]}
            elif key in return_keys:
                return key, tuple(line.return_value for line in selected)
            elif key in Binds.Select_All:
                selected = set(range(len(lines)))
            elif key in Binds.Deselect_All:
                selected.clear()
            else:
                assert False, "Got unhandled key as input {}".format(key)
        else:
            if key in select_keys:
                return key, lines[select_keys.index(key) + scroll_offset].return_value
            elif key in return_keys:
                return key, None
            else:
                assert False, "Got unhandled key as input {}".format(key)

def _get_vars(window, lines, multi_select, select_keys, return_keys):
    if select_keys:
        content_size = min(window.rows - 4, len(lines), len(select_keys))
    else:
        content_size = min(window.rows - 4, len(lines))

    select_keys = select_keys[:content_size]
    all_keys = Binds.ScrollKeys + select_keys + return_keys
    if multi_select:
        all_keys += Binds.MultiSelectKeys

    return content_size, select_keys, all_keys

def _get_print_lines(lines, offset, content_size, selected, select_keys):
    sliced_lines = _slice_lines(lines, offset, offset + content_size)
    if select_keys:
        return tuple("{} {} {}".format(key, "+" if line in selected else "-",
                     line.display) for key, line in zip(select_keys, sliced_lines))
    else:
        return tuple(line.display for line in sliced_lines)

def _selection_symbol(selected, index):
    return "+" if index in selected else "-"

def _capitalize_single_chars(seq):
    for key in seq:
        if len(key) == 1:
            yield key.upper()
        else:
            yield key

def _print_view(window, print_lines, header="", footer="",
                main_view_pos=2, header_pos=0, footer_pos=-1):
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
    if key in Binds.Next_Line:
        offset += 1
    elif key in Binds.Next_Page:
        offset += visible_amount - 1
    elif key in Binds.Previous_Line:
        offset -= 1
    elif key in Binds.Previous_Page:
        offset -= visible_amount - 1
    max_offset = max(0, lines_amount - visible_amount)
    offset = min(max(0, offset), max_offset)
    return offset
