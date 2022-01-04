from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T', covariant=True)
@dataclass(slots=True, order=True, frozen=True)
class Line(Generic[T]):
    """line_view Line"""
    display: str
    return_value: T
