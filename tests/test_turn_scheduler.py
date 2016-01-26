from __future__ import absolute_import, division, print_function, unicode_literals

from turn_scheduler import TurnScheduler


def test_turn_scheduler():
    ts = TurnScheduler()
    ts.add("D", 2)
    ts.add("C", 1)
    ts.add("B", 1)
    ts.add("X", 1)
    ts.add("A", 0)
    ts.remove("X")

    assert ts.advance_time() == ("A", 0)
    assert ts.advance_time() == ("B", 1)
    ts.add("B", 0)
    assert ts.advance_time() == ("B", 0)
    ts.add("B", 0)
    assert ts.advance_time() == ("B", 0)
    assert ts.advance_time() == ("C", 0)
    assert ts.advance_time() == ("D", 1)

    ts.add("E", 20)

    assert ts.advance_time() == ("E", 20)
