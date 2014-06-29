import rdg


def test_rectangle():
    rect = rdg.Rectangle(9, 9, -10, -10)
    assert rect == (0, 0, 10, 10)
