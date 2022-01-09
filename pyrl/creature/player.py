from __future__ import annotations

from dataclasses import dataclass

from pyrl.creature.mixins.hoarder import Hoarder
from pyrl.creature.mixins.learner import Learner
from pyrl.creature.mixins.visionary import Visionary

@dataclass(eq=False)
class Player(Hoarder, Visionary, Learner):
    pass
