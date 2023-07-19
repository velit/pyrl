import logging
from collections import Counter

from pyrl.engine.creature.player import Player
from pyrl.engine.creature.skills import Skills, Skill
from pyrl.engine.creature.stats import Stat
from pyrl.game_data.pyrl_player import pyrl_player


def test_player() -> None:
    skills = Skills(Counter({Skill.HEALING: 40}))
    player = Player(skills, "player")
    logging.debug(player)
    logging.debug(player.stats)
    assert player[Stat.STR]    == 11
    assert player[Stat.DEX]    == 11
    assert player[Stat.INT]    == 11
    assert player[Stat.END]    == 11
    assert player[Stat.PER]    == 11
    assert player[Stat.ACC]    == 16
    assert player[Stat.ARMOR]  == 1
    assert player[Stat.DMG]    == 3
    assert player[Stat.DEF]    == 16
    assert player[Stat.MAX_HP] == 16
    assert player[Stat.REGEN]  == 3
    assert player[Stat.SIGHT]  == 5
    assert player[Stat.SPEED]  == 100

def test_pyrl_player() -> None:
    player = pyrl_player()
    logging.debug(player)
    logging.debug(player.stats)
    assert player[Stat.STR]    == 11
    assert player[Stat.DEX]    == 11
    assert player[Stat.INT]    == 11
    assert player[Stat.END]    == 13
    assert player[Stat.PER]    == 11
    assert player[Stat.ACC]    == 26
    assert player[Stat.ARMOR]  == 1021
    assert player[Stat.DMG]    == 3
    assert player[Stat.DEF]    == 1028
    assert player[Stat.MAX_HP] == 18
    assert player[Stat.REGEN]  == 2
    assert player[Stat.SIGHT]  == 5
    assert player[Stat.SPEED]  == 200
