from __future__ import absolute_import, division, print_function, unicode_literals

from generic_structures import PriorityQueue, List2D


def test_List2D():
    l = List2D((), 2)
    assert l.get_dimensions() == (0, 2)

    l.append(0)
    assert l.get_dimensions() == (1, 2)

    l.append(1)
    assert l.get_dimensions() == (1, 2)

    l.append(2)
    assert l.get_dimensions() == (2, 2)

    l.append(3)
    assert l.get_dimensions() == (2, 2)

    l.append(4)
    assert l.get_dimensions() == (3, 2)

    l[l.get_coord(0)] == 0
    l[l.get_coord(1)] == 1
    l[l.get_coord(2)] == 2
    l[l.get_coord(3)] == 3
    l[l.get_coord(4)] == 4


def test_turn_scheduler():
    pq = PriorityQueue()
    pq.add(3, 3)
    pq.add(1, 1)
    pq.add(2, 2)
    pq.add(0, 0)
    pq.remove(2)

    assert pq.pop() == (0, 0, 4)
    assert pq.pop() == (1, 1, 2)
    assert pq.pop() == (3, 3, 1)
