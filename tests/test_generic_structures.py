import pytest

from pyrl.generic_structures import Array2D, Event, OneToOneMapping

def test_array():
    dims = 2, 2
    array = Array2D(dims, (0, 1, 2))
    assert array.dimensions == dims

    assert array[array.get_coord(0)] == 0
    assert array[array.get_coord(1)] == 1
    assert array[array.get_coord(2)] == 2
    assert array[array.get_coord(3)] is None

    assert array.is_legal((0, 0))
    assert array.is_legal((1, 1))

    assert not array.is_legal((-1, -1))
    assert not array.is_legal((3, 2))

def test_one_to_one_mapping():
    mapping = OneToOneMapping()
    mapping[0] = 0
    mapping[1] = 1
    mapping[2] = 2
    mapping[3] = 3
    mapping[4] = 4

    assert mapping[0] == 0
    assert mapping[1] == 1
    assert mapping[2] == 2
    assert mapping[3] == 3
    assert mapping[4] == 4

    mapping[0] = 5
    assert mapping[0] == 5
    assert mapping.getkey(5) == 0

    with pytest.raises(ValueError):
        mapping[1] = 5

    del mapping[4]
    with pytest.raises(KeyError):
        mapping.getkey(4)

    with pytest.raises(ValueError):
        mapping.update(**{"a": 10, "b": 10})

    with pytest.raises(ValueError):
        mapping.update({"a": 10, "b": 10})

def test_observable_event():
    event = Event()
    sub1 = None
    sub2 = None

    def sub_fun_1(x):
        nonlocal sub1
        sub1 = x

    def sub_fun_2(x):
        nonlocal sub2
        sub2 = x

    event.subscribe(sub_fun_1)
    event.subscribe(sub_fun_2)

    event.trigger(10)

    assert sub1 == sub2 == 10
