from pyrl.turn_scheduler import TurnScheduler


def test_turn_scheduler():
    ts = TurnScheduler()
    ts.add("D", 2)
    ts.add("C", 1)
    ts.add("B", 1)
    ts.add("X", 1)
    ts.add("A", 0)
    ts.remove("X")

    assert ts.advance_time() == ("A", 0)
    ts.addpop("A", 20)
    assert ts.advance_time() == ("B", 1)
    ts.addpop("B", 0)
    assert ts.advance_time() == ("B", 0)
    ts.addpop("B", 0)
    assert ts.advance_time() == ("B", 0)
    ts.addpop("B", 19)
    assert ts.advance_time() == ("C", 0)
    ts.addpop("C", 19)
    assert ts.advance_time() == ("D", 1)
    ts.addpop("D", 18)

    ts.add("E", 18)

    assert ts.advance_time() == ("E", 18)
    ts.addpop("E", 1)
    assert ts.advance_time() == ("D", 0)
    ts.addpop("D", 1)
    assert ts.advance_time() == ("C", 0)
    ts.addpop("C", 1)
    assert ts.advance_time() == ("B", 0)
    ts.addpop("B", 1)
    assert ts.advance_time() == ("A", 0)
    ts.addpop("A", 1)
