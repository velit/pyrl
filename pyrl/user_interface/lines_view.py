from __future__ import annotations

import re
from collections.abc import Sequence, Iterable
from typing import TypeVar

from pyrl.config.binds import Binds
from pyrl.types.keys import Key, KeyTuple
from pyrl.types.line import Line
from pyrl.window.base_window import BaseWindow

def build_lines(iterable: Iterable[str]) -> tuple[Line[int], ...]:
    return tuple(Line(value, i) for i, value in enumerate(iterable))

def define_footers() -> tuple[str, str]:
    pages = f"{Binds.Next_Page.key}/{Binds.Previous_Page.key} scroll"
    lines = f"{Binds.Next_Line.key}/{Binds.Previous_Line.key} next/previous line"
    selects = f"{Binds.Deselect_All.key}/{Binds.Select_All.key} (de)select all"
    filt = f"{Binds.Filter.key} filter"
    close = f"{Binds.Cancel.key} close"

    single_footer = f"{pages}  {lines}  {filt}  {close}"
    multi_footer = f"{pages}  {lines}  {selects}  {filt}  {close}"
    return single_footer, multi_footer

single_select_footer, multi_select_footer = define_footers()

S = TypeVar('S')
def lines_view(window: BaseWindow, lines: Sequence[Line[S]],
               return_keys: KeyTuple = Binds.Cancel, select_keys: KeyTuple = (),
               header: str = "", footer: str | None = None) -> tuple[Key, S]:
    return _lines_view(window, lines, False, return_keys, select_keys, header, footer)

M = TypeVar('M')
def multi_select_lines_view(window: BaseWindow, lines: Sequence[Line[M]],
                            return_keys: KeyTuple = Binds.Cancel, select_keys: KeyTuple = (),
                            header: str = "", footer: str | None = None) -> tuple[Key, Sequence[M]]:
    return _lines_view(window, lines, True, return_keys, select_keys, header, footer)

T = TypeVar('T')
def _lines_view(window: BaseWindow, lines: Sequence[Line[T]], multi_select: bool = False,
                return_keys: KeyTuple = Binds.Cancel, select_keys: KeyTuple = (),
                header: str = "", footer: str | None = None) -> tuple[Key, T | None] | tuple[Key, Sequence[T]]:
    """
    Render a view based on parameter lines which is a sequence of Line namedtuples.

    In normal mode returns (return_key, possible_selected_item), item == None if returned
    by return key.
    In multi_select mode returns (return_key, selected_items)
    """
    if footer is None:
        footer = multi_select_footer if multi_select else single_select_footer

    orig_lines = tuple(lines)
    orig_select_keys = tuple(select_keys)
    scroll_offset = 0
    selected: set[Line] = set()
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
                filter_regex = f" (Filter/{filter_regex})"
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
                selected = set(lines)
            elif key in Binds.Deselect_All:
                selected.clear()
            else:
                assert False, f"Unhandled {key=}"
        else:
            if key in select_keys:
                return key, lines[select_keys.index(key) + scroll_offset].return_value
            elif key in return_keys:
                return key, None
            else:
                assert False, f"Unhandled {key=}"

A = TypeVar('A')
def _get_vars(window: BaseWindow, lines: Sequence[Line[A]], multi_select: bool,
              select_keys: KeyTuple, return_keys: KeyTuple) -> tuple[int, KeyTuple, KeyTuple]:
    if select_keys:
        content_size = min(window.rows - 4, len(lines), len(select_keys))
    else:
        content_size = min(window.rows - 4, len(lines))

    select_keys = select_keys[:content_size]
    all_keys = tuple(Binds.ScrollKeys) + select_keys + return_keys
    if multi_select:
        all_keys += Binds.MultiSelectKeys

    return content_size, select_keys, all_keys

B = TypeVar('B')
def _get_print_lines(lines: Sequence[Line[B]], offset: int, content_size: int,
                     selected: set[Line[B]], select_keys: KeyTuple) -> Sequence[str]:
    sliced_lines = _slice_lines(lines, offset, offset + content_size)
    if select_keys:
        return tuple(f"{key} {'+' if line in selected else '-'} {line.display}"
                     for key, line in zip(select_keys, sliced_lines))
    else:
        return tuple(line.display for line in sliced_lines)

C = TypeVar('C')
def _slice_lines(seq: Sequence[S], start_index: int = 0, stop_index: int | None = None) -> Iterable[S]:
    if stop_index is not None:
        for i in range(start_index, stop_index):
            yield seq[i]
    else:
        for i in range(start_index, len(seq)):
            yield seq[i]

def _print_view(window: BaseWindow, print_lines: Iterable[str], header: str = "", footer: str = "",
                main_view_pos: int = 2, header_pos: int = 0, footer_pos: int = -1) -> None:
    window.clear()
    if header is not None:
        window.draw_banner(header, y_offset=header_pos)
    window.draw_lines(print_lines, y_offset=main_view_pos)
    if footer is not None:
        window.draw_banner(footer, y_offset=footer_pos)

def _new_offset(offset: int, key: Key, visible_amount: int, lines_amount: int) -> int:
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
