from __future__ import annotations

from collections import defaultdict
from typing import Any, TYPE_CHECKING

from pyrl.creature.creature import Creature

if TYPE_CHECKING:
    from pyrl.types.coord import Coord
    from pyrl.world.level import Level

class Visionary(Creature):

    """Creatures with this mixin class remember the level squares they've seen."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.visited_locations: dict[Level, set[Coord]] = defaultdict(set)
        self._vision: set[Coord] = set()

    def get_visited_locations(self) -> set[Coord]:
        return self.visited_locations[self.level]

    @property
    def vision(self) -> set[Coord]:
        return self._vision

    @vision.setter
    def vision(self, coordinates: set[Coord]) -> None:
        self._vision = coordinates
        self.visited_locations[self.level] |= coordinates

    @vision.deleter
    def vision(self) -> None:
        del self._vision
