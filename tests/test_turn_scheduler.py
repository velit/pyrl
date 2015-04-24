from __future__ import absolute_import, division, print_function, unicode_literals

from turn_scheduler import TurnScheduler


def test_turn_scheduler():
    ts = TurnScheduler()
    ts.add(3, 1)
    ts.add(1, 1)
    ts.add(2, 1)
    ts.add(0, 1)
    ts.remove(2)

    assert ts.advance_time() == (3, 1)
    assert ts.advance_time() == (1, 0)
    assert ts.advance_time() == (0, 0)

    ts.add(3, 20)

    assert ts.advance_time() == (3, 20)
