from __future__ import annotations

import random
from collections.abc import Iterable, Container
from dataclasses import dataclass, field, InitVar
from typing import TYPE_CHECKING

from pyrl.config.debug import Debug
from pyrl.engine.actions.action import Action
from pyrl.engine.behaviour.coordinates import bresenham, cross_product, add_vector
from pyrl.engine.behaviour.pathing import path, distance
from pyrl.engine.creature.creature_picker import CreaturePicker
from pyrl.engine.world.item import Item
from pyrl.engine.creature.enums.stats import Stat
from pyrl.engine.structures.dimensions import Dimensions
from pyrl.engine.structures.event import Event
from pyrl.engine.structures.helper_mixins import DimensionsMixin
from pyrl.engine.structures.scheduler import Scheduler
from pyrl.engine.structures.table import Table
from pyrl.engine.structures.uniq_dict import UniqDict
from pyrl.engine.enums.directions import Direction, Dir, Coord
from pyrl.engine.enums.glyphs import Glyph
from pyrl.engine.world.enums.level_key import LevelKey
from pyrl.engine.world.enums.world_point import WorldPoint
from pyrl.engine.world.enums.level_location import LevelLocation
from pyrl.game_data.levels.shared_assets import DefaultLocation
from pyrl.game_data.pyrl_creatures import PyrlCreature

if TYPE_CHECKING:
    from pyrl.engine.world.tile import Tile
    from pyrl.engine.creature.creature import Creature

@dataclass(eq=False, slots=True)
class Level(DimensionsMixin):

    # __init__
    level_key: LevelKey
    area_level: int
    tiles: Table[Tile]                            = field(repr=False)
    locations: UniqDict[Coord, LevelLocation]     = field(default_factory=UniqDict)
    custom_creatures: InitVar[Iterable[Creature]] = field(repr=False, default=())
    initial_creature_spawns: InitVar[bool]        = True
    ongoing_creature_spawns: bool                 = True

    # rest
    creature_picker: CreaturePicker      = field(init=False, repr=False)
    creatures: dict[Coord, Creature]     = field(init=False, repr=False, default_factory=dict)
    items: dict[Coord, tuple[Item, ...]] = field(init=False, repr=False, default_factory=dict)
    turn_scheduler: Scheduler[Creature]  = field(init=False, repr=False, default_factory=Scheduler)
    visible_change: Event                = field(init=False, repr=False, default_factory=Event)

    def __post_init__(self, custom_creatures: Iterable[Creature], initial_creature_spawns: bool) -> None:
        self.creature_picker = CreaturePicker.using_speciation(PyrlCreature.templates(), self.area_level)

        for creature in custom_creatures:
            self.spawn_creature(creature)

        creature_spawn_count = 99
        if initial_creature_spawns:
            for _ in range(creature_spawn_count):
                creature = self.creature_picker.spawn_random_creature()
                self.spawn_creature(creature)

    @property
    def dimensions(self) -> Dimensions:
        return self.tiles.dimensions

    def get_location_coord(self, level_location: LevelLocation) -> Coord:
        if level_location == DefaultLocation.Random_Location:
            return self.free_coord()
        else:
            return self.locations.getkey(level_location)

    def free_coord(self) -> Coord:
        for _ in range(Debug.max_loop_cycles):
            coord = self.tiles.random_coord()
            if self.is_passable(coord):
                return coord

        free_coords = [coord for coord in self.tiles.coord_iter() if self.is_passable(coord)]
        if free_coords:
            return random.choice(free_coords)
        else:
            assert False, "Free coord search failed."

    def visible_glyph(self, coord: Coord) -> Glyph:
        if coord in self.creatures:
            return self.creatures[coord].glyph
        elif coord in self.items:
            return self.items[coord][0].glyph
        else:
            return self.tiles[coord].visible_glyph

    def memory_glyph(self, coord: Coord) -> Glyph:
        return self.tiles[coord].memory_glyph

    def get_vision_information(self, coords: Iterable[Coord], visible_coords: Container[Coord],
                               always_show_creatures: bool = False) -> Iterable[tuple[Coord, Glyph]]:
        for coord in coords:
            if coord in visible_coords:
                yield coord, self.visible_glyph(coord)
            else:
                if always_show_creatures and coord in self.creatures:
                    yield coord, self.creatures[coord].glyph
                else:
                    yield coord, self.memory_glyph(coord)

    def get_last_pathable_coord(self, coord_start: Coord, coord_end: Coord) -> Coord | None:
        last = None
        for coord in bresenham(coord_start, coord_end):
            if not self.is_pathable(coord):
                break
            last = coord
        return last

    def get_neighbor_location_coords_and_costs(self, coord: Coord) -> Iterable[tuple[Coord, int]]:
        for direction in self.get_passable_neighbors(coord):
            neighbor_coord = add_vector(coord, direction)
            multiplier = self.movement_multiplier(coord, direction)
            yield neighbor_coord, round(multiplier * Action.Move.base_cost)

    def get_passable_neighbors(self, coord: Coord) -> Iterable[Direction]:
        for direction in Dir.All:
            neighbor_coord = add_vector(coord, direction)
            if self.is_legal(neighbor_coord) and self.tiles[neighbor_coord].is_passable:
                yield direction

    def is_legal(self, coord: Coord) -> bool:
        return self.tiles.is_legal(coord)

    def is_passable(self, coord: Coord) -> bool:
        if coord in self.creatures:
            return False
        else:
            return self.tiles[coord].is_passable

    def is_pathable(self, coord: Coord) -> bool:
        return self.tiles[coord].is_passable

    def is_see_through(self, coord: Coord) -> bool:
        return self.tiles[coord].is_see_through

    def check_los(self, coord_a: Coord, coord_b: Coord) -> bool:
        return (all(self.is_see_through(coord) for coord in bresenham(coord_a, coord_b))
                or all(self.is_see_through(coord) for coord in bresenham(coord_b, coord_a)))

    def distance(self, coord_a: Coord, coord_b: Coord) -> int:
        return round(distance(coord_a, coord_b, Action.Move.base_cost, Dir.DiagonalMoveMult))

    def movement_multiplier(self, coord: Coord, direction: Direction) -> float:
        origin_tile_multiplier = self.tiles[coord].move_multi
        target_coord = add_vector(coord, direction)
        target_tile_multiplier = self.tiles[target_coord].move_multi

        tile_multiplier = (origin_tile_multiplier + target_tile_multiplier) / 2
        return tile_multiplier * self.direction_multiplier(direction)

    def direction_multiplier(self, direction: Direction) -> float:
        if direction in Dir.Orthogonals:
            return Dir.OrthogonalMoveMult
        elif direction in Dir.Diagonals:
            return Dir.DiagonalMoveMult
        elif direction == Dir.Stay:
            return Dir.StayMoveMult
        assert False, f"Invalid {direction=}"

    # nudge_coord nudges towards a line between end_coord and nudge_coord
    def _a_star_heuristic(self, start_coord: Coord, end_coord: Coord, nudge_coord: Coord) -> float:
        cost: float = self.distance(start_coord, end_coord)
        if Debug.cross:
            cost += cross_product(start_coord, end_coord, nudge_coord) / Debug.cross_mod
        return cost

    def path(self, start_coord: Coord, goal_coord: Coord) -> Iterable[Coord]:
        return path(start_coord, goal_coord, self.get_neighbor_location_coords_and_costs, self._a_star_heuristic)

    def look_information(self, coord: Coord) -> str:
        # if coord in creature.visited_location_coords:
        information = f"{coord[0]}x{coord[1]} "
        if coord in self.creatures:
            c: Creature = self.creatures[coord]
            damage = c.damage_dice
            information += f"{c.name} hp:{c.hp}/{c[Stat.MAX_HP]} sight:{c[Stat.SIGHT]} armor:{c[Stat.ARMOR]} dr:{c[Stat.DEF]} ar:{c[Stat.ACC]} attack:{damage.dices}D{damage.faces}+{damage.addition}"
        else:
            information += self.tiles[coord].name
        return information
        # else:
        #     return "You don't know anything about this place."

    def get_world_point(self, coord: Coord) -> WorldPoint:
        return WorldPoint(self.level_key, self.locations[coord])

    def spawn_creature(self, creature: Creature) -> None:
        coord = None
        if hasattr(creature, "coord"):
            assert self.is_passable(creature.coord), \
                f"Attempting to spawn {creature.name} to already occupied square: {creature.coord}"
            coord = creature.coord

        self.add_creature(creature, coord)
        self.turn_scheduler.add(creature, creature.action_cost(Action.Spawn))

    def add_creature(self, creature: Creature, coord: Coord | None = None) -> None:
        if coord is None:
            coord = self.free_coord()
        if coord in self.creatures:
            blocking_creature = self.creatures[coord]
            self.move_creature(blocking_creature, self.free_coord())
        self.creatures[coord] = creature
        creature.coord = coord
        creature.level = self
        self.visible_change.trigger(coord)

    def move_creature_to_location(self, creature: Creature, level_location: LevelLocation) -> None:
        creature.level.remove_creature(creature)
        coord = self.get_location_coord(level_location)
        self.add_creature(creature, coord)

    def remove_creature(self, creature: Creature) -> None:
        coord = creature.coord
        del self.creatures[coord]
        self.turn_scheduler.remove(creature)
        self.visible_change.trigger(coord)

    def move_creature(self, creature: Creature, new_coord: Coord) -> None:
        old_coord = creature.coord
        del self.creatures[old_coord]
        self.creatures[new_coord] = creature
        creature.coord = new_coord

        self.visible_change.trigger(old_coord)
        self.visible_change.trigger(new_coord)

    def move_creature_to_dir(self, creature: Creature, direction: Direction) -> None:
        target_coord = add_vector(creature.coord, direction)
        self.move_creature(creature, target_coord)

    def swap_creature(self, creature_a: Creature, creature_b: Creature) -> None:
        creature_a.coord, creature_b.coord = creature_b.coord, creature_a.coord
        self.creatures[creature_a.coord] = creature_a
        self.creatures[creature_b.coord] = creature_b
        self.visible_change.trigger(creature_a.coord)
        self.visible_change.trigger(creature_b.coord)

    def inspect_items(self, coord: Coord) -> tuple[Item, ...]:
        if coord in self.items:
            return tuple(self.items[coord])
        else:
            return ()

    def pop_items(self, coord: Coord, item_indexes: Iterable[int]) -> tuple[Item, ...]:
        if not item_indexes:
            return ()

        assert coord in self.items, f"Trying to take items from {coord=} that doesn't have any."

        current_items = self.items[coord]
        taken_items = tuple(current_items[index] for index in item_indexes)

        index_set = set(item_indexes)
        left_items = tuple(item for index, item in enumerate(current_items) if index not in index_set)

        if left_items:
            self.items[coord] = left_items
        else:
            del self.items[coord]

        self.visible_change.trigger(coord)
        return taken_items

    def add_items(self, coord: Coord, items: tuple[Item, ...]) -> None:
        if coord in self.items:
            current_items = self.items[coord]
        else:
            current_items = ()
        self.items[coord] = current_items + items
        self.visible_change.trigger(coord)
