from __future__ import annotations

from collections import defaultdict
from dataclasses import field, dataclass
from typing import TYPE_CHECKING

from pyrl.creature.creature import Creature
from pyrl.world.level import Level

if TYPE_CHECKING:
    from pyrl.types.coord import Coord

@dataclass(eq=False)
class Visionary(Creature):
    """Creatures with this mixin class see and remember squares they've seen."""

    seen_coords: dict[Level, set[Coord]] = field(init=False, repr=False, default_factory=lambda: defaultdict(set))
    _vision: set[Coord]                  = field(init=False, repr=False, default_factory=set)

    def get_visited_locations(self) -> set[Coord]:
        return self.seen_coords[self.level]

    @property
    def vision(self) -> set[Coord]:
        return self._vision

    @vision.setter
    def vision(self, coordinates: set[Coord]) -> None:
        self._vision = coordinates
        self.seen_coords[self.level] |= coordinates

    @vision.deleter
    def vision(self) -> None:
        del self._vision
