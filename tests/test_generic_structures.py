from generic_structures import PriorityQueue


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
