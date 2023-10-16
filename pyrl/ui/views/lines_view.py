from __future__ import annotations

import re
from collections.abc import Sequence, Iterable
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Final

from pyrl.config.binds import Binds
from pyrl.engine.enums.glyphs import ColorPair, ColorStr
from pyrl.engine.enums.keys import AnyKey, KeyTuple
from pyrl.ui.views.line import Line
from pyrl.ui.window.base_window import BaseWindow

def build_lines(iterable: Iterable[str]) -> tuple[Line[int], ...]:
    return tuple(Line(value, i) for i, value in enumerate(iterable))

def build_color_lines(iterable: Iterable[tuple[str, ColorPair]]) -> tuple[Line[int], ...]:
    return tuple(Line(value, i, color) for i, (value, color) in enumerate(iterable))

T = TypeVar('T')
def lines_view(window: BaseWindow, lines: Sequence[Line[T]], select_keys: KeyTuple = (),
               return_keys: KeyTuple = Binds.Cancel, header: str = "",
               footer: str | None = None) -> tuple[AnyKey, T | None]:
    return LinesView(window, lines, select_keys, return_keys, header, footer).single()

def multi_select_lines_view(window: BaseWindow, lines: Sequence[Line[T]], select_keys: KeyTuple = (),
                            return_keys: KeyTuple = Binds.Cancel, header: str = "",
                            footer: str | None = None) -> tuple[AnyKey, Sequence[T]]:
    return LinesView(window, lines, select_keys, return_keys, header, footer).multi()

@dataclass(eq=False)
class LinesView(Generic[T]):
    """
    Render a Lines based view with given parameters.

    lines The objects associated with Lines are returned if those lines are selected by the user
    select_keys defines which keys are valid for selecting lines
    return_keys will cause the view to return either selected lines or None in single mode
    header is printed as is
    footer is printed, if it's None a default footer that depends on the mode is printed
    """
    window: Final[BaseWindow] = field(repr=False)
    orig_lines: Sequence[Line[T]] = field(repr=False)
    orig_select_keys: Final[KeyTuple] = field(default_factory=tuple, repr=False)
    return_keys: Final[KeyTuple] = Binds.Cancel
    header: Final[str] = ""
    footer: str | None = None

    selected: set[Line[T]] = field(default_factory=set, init=False)
    scroll_offset: int = field(default=0, init=False)
    filter_regex_visual: str = field(default="", init=False)

    lines: Sequence[Line[T]] = field(init=False)
    select_keys: KeyTuple = field(init=False)
    all_keys: KeyTuple = field(init=False)
    content_size: int = field(init=False)

    single_footer: str = field(init=False, repr=False)
    multi_footer: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.lines = self.orig_lines
        self._init_footers()

    def _init_footers(self) -> None:
        pages = f"{Binds.Next_Page.key}/{Binds.Previous_Page.key} scroll"
        lines = f"{Binds.Next_Line.key}/{Binds.Previous_Line.key} next/previous line"
        selects = f"{Binds.Deselect_All.key}/{Binds.Select_All.key} (de)select all"
        filt = f"{Binds.Filter.key} filter"
        close = f"{Binds.Cancel.key} close"

        self.single_footer = f"{pages}  {lines}  {filt}  {close}"
        self.multi_footer = f"{pages}  {lines}  {selects}  {filt}  {close}"

    def single(self) -> tuple[AnyKey, T | None]:
        if self.footer is None:
            self.footer = self.single_footer

        while True:
            self._update_vars(multi_select=False)
            self._print_view(self.header + self.filter_regex_visual, self.footer)
            key = self.window.get_key(keys=self.all_keys, refresh=True)

            if key in Binds.Filter:
                self._handle_filter()
            elif key in Binds.ScrollKeys:
                self._handle_scrolling(key)
            else:
                if key in self.select_keys:
                    return key, self.lines[self.select_keys.index(key) + self.scroll_offset].return_value
                elif key in self.return_keys:
                    return key, None
                else:
                    assert False, f"Unhandled {key=}"

    def multi(self) -> tuple[AnyKey, Sequence[T]]:
        """
        Render a view based on parameter lines which is a sequence of Line namedtuples.

        In normal mode returns (return_key, possible_selected_item), item == None if returned
        by return key.
        In multi_select mode returns (return_key, selected_items)
        """
        if self.footer is None:
            self.footer = self.multi_footer

        while True:
            self._update_vars(multi_select=True)
            self._print_view(self.header + self.filter_regex_visual, self.footer)
            key = self.window.get_key(keys=self.all_keys, refresh=True)

            if key in Binds.Filter:
                self._handle_filter()
            elif key in Binds.ScrollKeys:
                self._handle_scrolling(key)
            else:
                if key in self.select_keys:
                    self.selected ^= {self.lines[self.select_keys.index(key) + self.scroll_offset]}
                elif key in self.return_keys:
                    return key, tuple(line.return_value for line in self.selected)
                elif key in Binds.Select_All:
                    self.selected = set(self.lines)
                elif key in Binds.Deselect_All:
                    self.selected.clear()
                else:
                    assert False, f"Unhandled {key=}"

    def _handle_filter(self) -> None:
        query = "Filter regex (empty to clear): "
        filter_regex = self.window.get_str(query, (1, 0))
        self.window.draw_str(" " * (len(query + filter_regex) + 1), (1, 0))
        if filter_regex:
            self.lines = tuple(line for line in self.orig_lines if re.search(filter_regex, line.display))
            self.filter_regex_visual = f" (Filter/{filter_regex})"
        else:
            self.lines = self.orig_lines
        self.scroll_offset = 0

    def _update_vars(self, multi_select: bool) -> None:
        """Return the size left for content and update current select and all keys"""
        if self.orig_select_keys:
            self.content_size = min(self.window.rows - 4, len(self.lines), len(self.orig_select_keys))
        else:
            self.content_size = min(self.window.rows - 4, len(self.lines))

        self.select_keys = self.orig_select_keys[:self.content_size]
        self.all_keys = tuple(Binds.ScrollKeys) + self.select_keys + self.return_keys
        if multi_select:
            self.all_keys += Binds.MultiSelectKeys

    def _get_print_lines(self) -> Sequence[ColorStr]:
        """Return a sequence of printable lines from given parameters."""
        sliced_lines = self.lines[self.scroll_offset: self.scroll_offset + self.content_size]
        if self.select_keys:
            return tuple((f"{key} {'+' if line in self.selected else '-'} {line.display}", line.color)
                         for key, line in zip(self.select_keys, sliced_lines))
        else:
            return tuple((line.display, line.color) for line in sliced_lines)

    def _print_view(self, header: str, footer: str,
                    main_view_pos: int = 2, header_pos: int = 0, footer_pos: int = -1) -> None:
        self.window.clear()
        if header is not None:
            self.window.draw_banner(header, y_offset=header_pos)
        self.window.draw_lines(self._get_print_lines(), y_offset=main_view_pos)
        if footer is not None:
            self.window.draw_banner(footer, y_offset=footer_pos)

    def _handle_scrolling(self, key: AnyKey) -> None:
        """Calculate the next offset from the given input key."""
        if key in Binds.Next_Line:
            self.scroll_offset += 1
        elif key in Binds.Next_Page:
            self.scroll_offset += self.content_size - 1
        elif key in Binds.Previous_Line:
            self.scroll_offset -= 1
        elif key in Binds.Previous_Page:
            self.scroll_offset -= self.content_size - 1
        max_offset = max(0, len(self.lines) - self.content_size)
        self.scroll_offset = min(max(0, self.scroll_offset), max_offset)
