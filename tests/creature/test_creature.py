from pyrl.creature.creature import Creature
from pyrl.enums.colors import Pair
from decimal import Decimal

def test_danger_level_spawn_mult():
    c = Creature("test", ('t', Pair.Cyan), danger_level=0)

    assert c.danger_level_spawn_mult(-6) == Decimal(0)
    assert c.danger_level_spawn_mult(-5) == Decimal(0)
    assert c.danger_level_spawn_mult(-4) == Decimal("0.008")
    assert c.danger_level_spawn_mult(-3) == Decimal("0.064")
    assert c.danger_level_spawn_mult(-2) == Decimal("0.216")
    assert c.danger_level_spawn_mult(-1) == Decimal("0.512")
    assert c.danger_level_spawn_mult(0)  == Decimal(1)
    assert c.danger_level_spawn_mult(1)  == Decimal(1)
    assert c.danger_level_spawn_mult(2)  == Decimal(1)
    assert c.danger_level_spawn_mult(3)  == Decimal(1)
    assert c.danger_level_spawn_mult(4)  == Decimal(1)
    assert c.danger_level_spawn_mult(5)  == Decimal(1)
    assert c.danger_level_spawn_mult(6)  == Decimal(1)
    assert c.danger_level_spawn_mult(7)  == Decimal(1)
    assert c.danger_level_spawn_mult(8)  == Decimal(1)
    assert c.danger_level_spawn_mult(9)  == Decimal(1)
    assert c.danger_level_spawn_mult(10) == Decimal(1)
    assert c.danger_level_spawn_mult(11) == Decimal("0.999")
    assert c.danger_level_spawn_mult(12) == Decimal("0.992")
    assert c.danger_level_spawn_mult(13) == Decimal("0.973")
    assert c.danger_level_spawn_mult(14) == Decimal("0.936")
    assert c.danger_level_spawn_mult(15) == Decimal("0.875")
    assert c.danger_level_spawn_mult(16) == Decimal("0.784")
    assert c.danger_level_spawn_mult(17) == Decimal("0.657")
    assert c.danger_level_spawn_mult(18) == Decimal("0.488")
    assert c.danger_level_spawn_mult(19) == Decimal("0.271")
    assert c.danger_level_spawn_mult(20) == Decimal(0)
