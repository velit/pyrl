from __future__ import annotations

from pyrl.structures.scheduler import Scheduler

def test_turn_scheduler() -> None:
    ts: Scheduler[str] = Scheduler()
    ts.add("X", 1)
    ts.add("D", 2)
    ts.add("C", 1)
    ts.add("B", 1)
    ts.add("A", 0)
    ts.remove("X")

    assert ts.pop() == ("A", 0)
    ts.add("A", 20)
    assert ts.pop() == ("B", 1)
    ts.add("B", 0)
    assert ts.pop() == ("B", 0)
    ts.add("B", 0)
    assert ts.pop() == ("B", 0)
    ts.add("B", 19)
    assert ts.pop() == ("C", 0)
    ts.add("C", 19)
    assert ts.pop() == ("D", 1)
    ts.add("D", 18)

    ts.add("E", 18)

    assert ts.pop() == ("E", 18)
    ts.add("E", 1)
    assert ts.pop() == ("D", 0)
    ts.add("D", 1)
    assert ts.pop() == ("C", 0)
    ts.add("C", 1)
    assert ts.pop() == ("B", 0)
    ts.add("B", 1)
    assert ts.pop() == ("A", 0)
    ts.add("A", 1)
