from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Generic

from pyrl.types.color import ColorPair, Colors

T = TypeVar('T', covariant=True)
@dataclass(order=True, frozen=True)
class Line(Generic[T]):
    """line_view Line"""
    display: str
    return_value: T
    color: ColorPair = Colors.Normal
