from __future__ import annotations

from pyrl.algorithms.coord_algorithms import resize_range

def test_resize_in_range() -> None:
    assert resize_range(5, range(5, 9)) == 0
    assert resize_range(8, range(5, 9)) == 1

    assert resize_range(5, range(5, 9), range(10, 21)) == 10
    assert resize_range(8, range(5, 9), range(10, 21)) == 20
