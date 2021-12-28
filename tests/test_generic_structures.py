from __future__ import annotations

from collections.abc import Callable

import pytest

from pyrl.structures.dimensions import Dimensions
from pyrl.structures.event import Event
from pyrl.structures.one_to_one_mapping import OTOMap
from pyrl.structures.table import Table

def test_table() -> None:
    dims = Dimensions(2, 2)
    table = Table(dims, (0, 1, 2))
    assert table.dimensions == dims

    assert table[table.get_coord(0)] == 0
    assert table[table.get_coord(1)] == 1
    assert table[table.get_coord(2)] == 2
    assert table[table.get_coord(3)] is None

    assert table.is_legal((0, 0))
    assert table.is_legal((1, 1))

    assert not table.is_legal((-1, -1))
    assert not table.is_legal((3, 2))

def test_one_to_one_mapping() -> None:
    mapping: OTOMap[str, int] = OTOMap()
    mapping['0'] = 0
    mapping['1'] = 1
    mapping['2'] = 2
    mapping['3'] = 3
    mapping['4'] = 4

    assert mapping['0'] == 0
    assert mapping['1'] == 1
    assert mapping['2'] == 2
    assert mapping['3'] == 3
    assert mapping['4'] == 4

    mapping['0'] = 5
    assert mapping['0'] == 5
    assert mapping.getkey(5) == '0'

    with pytest.raises(ValueError):
        mapping['1'] = 5

    del mapping['4']
    with pytest.raises(KeyError):
        mapping.getkey(4)

    with pytest.raises(ValueError):
        mapping.update(a=10, b=10)

    with pytest.raises(ValueError):
        mapping.update({"a": 10, "b": 10})

def test_observable_event() -> None:
    event = Event()
    sub1 = None
    sub2 = None

    def sub_fun_1(x: Callable) -> None:
        nonlocal sub1
        sub1 = x

    def sub_fun_2(x: Callable) -> None:
        nonlocal sub2
        sub2 = x

    event.subscribe(sub_fun_1)
    event.subscribe(sub_fun_2)

    event.trigger(10)

    assert sub1 == sub2 == 10
