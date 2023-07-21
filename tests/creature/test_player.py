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
    assert player[Stat.STR]    == 10
    assert player[Stat.DEX]    == 10
    assert player[Stat.INT]    == 10
    assert player[Stat.END]    == 10
    assert player[Stat.PER]    == 10
    assert player[Stat.ACC]    == 15
    assert player[Stat.ARMOR]  == 1
    assert player[Stat.DMG]    == 3
    assert player[Stat.DEF]    == 15
    assert player[Stat.MAX_HP] == 15
    assert player[Stat.REGEN]  == 3
    assert player[Stat.SIGHT]  == 5
    assert player[Stat.SPEED]  == 100

def test_pyrl_player() -> None:
    player = pyrl_player()
    logging.debug(player)
    logging.debug(player.stats)
    assert player[Stat.STR]    == 10
    assert player[Stat.DEX]    == 10
    assert player[Stat.INT]    == 10
    assert player[Stat.END]    == 12
    assert player[Stat.PER]    == 10
    assert player[Stat.ACC]    == 25
    assert player[Stat.ARMOR]  == 1021
    assert player[Stat.DMG]    == 3
    assert player[Stat.DEF]    == 1027
    assert player[Stat.MAX_HP] == 17
    assert player[Stat.REGEN]  == 2
    assert player[Stat.SIGHT]  == 5
    assert player[Stat.SPEED]  == 200
