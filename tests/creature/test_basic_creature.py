import logging

from pyrl.engine.creature.basic_creature import BasicCreature
from pyrl.engine.creature.creature import Creature
from pyrl.engine.creature.stats import Stat
from pyrl.engine.types.glyphs import Colors


def test_basic_creature() -> None:
    c0 = BasicCreature.create("monster 0", ("m", Colors.Red), 0)
    logging.debug(c0)
    assert c0[Stat.STR]    == 10
    assert c0[Stat.DEX]    == 10
    assert c0[Stat.INT]    == 10
    assert c0[Stat.END]    == 10
    assert c0[Stat.PER]    == 10
    assert c0[Stat.ACC]    == 15
    assert c0[Stat.ARMOR]  == 1
    assert c0[Stat.DMG]    == 3
    assert c0[Stat.DEF]    == 15
    assert c0[Stat.MAX_HP] == 15
    assert c0[Stat.REGEN]  == 1
    assert c0[Stat.SIGHT]  == 5
    assert c0[Stat.SPEED]  == 100

    c10 = BasicCreature.create("monster 10", ("m", Colors.Red), 10)
    logging.debug(c10)
    assert c10[Stat.STR]    == 20
    assert c10[Stat.DEX]    == 20
    assert c10[Stat.INT]    == 20
    assert c10[Stat.END]    == 20
    assert c10[Stat.PER]    == 20
    assert c10[Stat.ACC]    == 30
    assert c10[Stat.ARMOR]  == 2
    assert c10[Stat.DMG]    == 6
    assert c10[Stat.DEF]    == 30
    assert c10[Stat.MAX_HP] == 30
    assert c10[Stat.REGEN]  == 2
    assert c10[Stat.SIGHT]  == 10
    assert c10[Stat.SPEED]  == 107

    c25 = BasicCreature.create("monster 25", ("m", Colors.Red), 25)
    logging.debug(c25)
    assert c25[Stat.STR]    == 35
    assert c25[Stat.DEX]    == 35
    assert c25[Stat.INT]    == 35
    assert c25[Stat.END]    == 35
    assert c25[Stat.PER]    == 35
    assert c25[Stat.ACC]    == 52
    assert c25[Stat.ARMOR]  == 3
    assert c25[Stat.DMG]    == 10
    assert c25[Stat.DEF]    == 52
    assert c25[Stat.MAX_HP] == 52
    assert c25[Stat.REGEN]  == 3
    assert c25[Stat.SIGHT]  == 13
    assert c25[Stat.SPEED]  == 117
