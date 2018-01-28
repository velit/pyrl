from enums.colors import Pair
from creature import Creature
from decimal import Decimal as D


def test_danger_level_spawn_mult():
    c = Creature("test", ('t', Pair.Cyan), danger_level=0)

    assert c.danger_level_spawn_mult(-6) == D(0)
    assert c.danger_level_spawn_mult(-5) == D(0)
    assert c.danger_level_spawn_mult(-4) == D("0.008")
    assert c.danger_level_spawn_mult(-3) == D("0.064")
    assert c.danger_level_spawn_mult(-2) == D("0.216")
    assert c.danger_level_spawn_mult(-1) == D("0.512")
    assert c.danger_level_spawn_mult(0) == D(1)
    assert c.danger_level_spawn_mult(1) == D(1)
    assert c.danger_level_spawn_mult(2) == D(1)
    assert c.danger_level_spawn_mult(3) == D(1)
    assert c.danger_level_spawn_mult(4) == D(1)
    assert c.danger_level_spawn_mult(5) == D(1)
    assert c.danger_level_spawn_mult(6) == D(1)
    assert c.danger_level_spawn_mult(7) == D(1)
    assert c.danger_level_spawn_mult(8) == D(1)
    assert c.danger_level_spawn_mult(9) == D(1)
    assert c.danger_level_spawn_mult(10) == D(1)
    assert c.danger_level_spawn_mult(11) == D("0.999")
    assert c.danger_level_spawn_mult(12) == D("0.992")
    assert c.danger_level_spawn_mult(13) == D("0.973")
    assert c.danger_level_spawn_mult(14) == D("0.936")
    assert c.danger_level_spawn_mult(15) == D("0.875")
    assert c.danger_level_spawn_mult(16) == D("0.784")
    assert c.danger_level_spawn_mult(17) == D("0.657")
    assert c.danger_level_spawn_mult(18) == D("0.488")
    assert c.danger_level_spawn_mult(19) == D("0.271")
    assert c.danger_level_spawn_mult(20) == D(0)
