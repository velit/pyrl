from __future__ import annotations

import itertools
import random
from collections.abc import Iterable
from functools import wraps
from typing import TYPE_CHECKING

from pyrl import path
from pyrl.config.debug import Debug
from pyrl.constants import dir
from pyrl.constants.coord import Coord
from pyrl.constants.level_gen import LevelGen
from pyrl.constants.level_location import LevelLocation
from pyrl.creature.actions import Action
from pyrl.creature.item import Item
from pyrl.game_data.default_creatures import default_creatures
from pyrl.game_data.levels.shared_assets import default_level_dimensions
from pyrl.generic_algorithms import bresenham, cross_product, add_vector
from pyrl.generic_structures import Event, Array2D, OneToOneMapping
from pyrl.rdg import generate_tiles_to
from pyrl.turn_scheduler import TurnScheduler

if TYPE_CHECKING:
    from pyrl.creature.creature import Creature

class CreatureSpawner:
    __slots__ = ('creatures', 'total_weight')

    def __init__(self):
        self.creatures = []
        self.total_weight = 0

    def set_creatures(self, creatures, danger_level):
        self.creatures = []
        accumulator = 0
        for creature in creatures:
            weight = creature.spawn_weight(danger_level)
            if weight == 0:
                continue
            accumulator += weight
            self.creatures.append((accumulator, creature))
        self.total_weight = accumulator

    def random_creature(self):
        assert len(self.creatures) != 0, "Trying to spawn a random creature with no creatures defined"
        index = random.randrange(self.total_weight)
        return next(creature for (slot, creature) in self.creatures if index < slot).copy()

class Level:

    def __init__(self, danger_level=0, generation_type=LevelGen.Dungeon, tiles=None,
                 locations=(), custom_creatures=(), creature_spawning_enabled=True):
        # Generation
        self.danger_level = danger_level
        self.generation_type = generation_type
        self.custom_creatures = list(custom_creatures)
        self.creature_spawn_count = 99
        self.creature_spawning_enabled = creature_spawning_enabled
        self.creature_spawner = CreatureSpawner()
        self.creature_spawn_list = []
        self.level_key = None

        # Normal usage
        if tiles is None:
            self.tiles = Array2D(default_level_dimensions)
        else:
            self.tiles = tiles

        self.locations = OneToOneMapping(locations)
        self.visible_change = Event()
        self.turn_scheduler = TurnScheduler()
        self.creatures = {}
        self.items = {}

        if self.generation_type.value > LevelGen.ExtendExisting.value:
            self.rows, self.cols = self.tiles.dimensions
        else:
            self.rows, self.cols = default_level_dimensions

        self.is_finalized = False

    def will_have_location(self, location):
        if location == LevelLocation.Random_Location:
            return True

        if location in self.locations.values():
            return True

        if self.generation_type != LevelGen.NoGeneration:
            return location in LevelLocation

        return False

    def get_creature_spawn_list(self):
        creature_list = []
        for creature in default_creatures:
            # creature_list.extend((creature, ) * creature.spawn_weight(self.danger_level))
            creature_list.append(creature)
        return creature_list

    def finalize(self, level_key):
        if self.generation_type.is_used():
            generate_tiles_to(self)

        self.level_key = level_key

        for creature in self.custom_creatures:
            self.spawn_creature(creature)

        if self.creature_spawning_enabled:
            self.creature_spawner.set_creatures(default_creatures, self.danger_level)

            for _ in range(self.creature_spawn_count):
                creature = self.creature_spawner.random_creature()
                self.spawn_creature(creature)
        else:
            self.creature_spawn_list = []

        self.is_finalized = True

    def get_location_coord(self, level_location):
        if level_location == LevelLocation.Random_Location:
            return self.free_coord()
        else:
            return self.locations.getkey(level_location)

    def free_coord(self):
        for _ in range(Debug.max_loop_cycles):
            coord = self.tiles.random_coord()
            if self.is_passable(coord):
                return coord

        free_coords = [coord for coord in self.tiles.coord_iter() if self.is_passable(coord)]
        if free_coords:
            return random.choice(free_coords)
        else:
            assert False, "Free coord search failed."

    def visible_char(self, coord):
        if coord in self.creatures:
            return self.creatures[coord].char
        elif coord in self.items:
            return self.items[coord][0].char
        else:
            return self.tiles[coord].visible_char

    def memory_char(self, coord):
        return self.tiles[coord].memory_char

    def get_vision_information(self, coords, visible_coords, always_show_creatures=False):
        for coord in coords:
            if coord in visible_coords:
                yield coord, self.visible_char(coord)
            else:
                if always_show_creatures and coord in self.creatures:
                    yield coord, self.creatures[coord].char
                else:
                    yield coord, self.memory_char(coord)

    def get_last_pathable_coord(self, coord_start, coord_end):
        last = None
        for coord in bresenham(coord_start, coord_end):
            if not self.is_pathable(coord):
                return last
            last = coord

    def get_neighbor_location_coords_and_costs(self, coord):
        for direction in self.get_passable_neighbors(coord):
            neighbor_coord = add_vector(coord, direction)
            multiplier = self.movement_multiplier(coord, direction)
            yield neighbor_coord, round(multiplier * Action.Move.base_cost)

    def get_passable_neighbors(self, coord):
        for direction in dir.All:
            neighbor_coord = add_vector(coord, direction)
            if self.is_legal(neighbor_coord) and self.tiles[neighbor_coord].is_passable:
                yield direction

    @wraps(Array2D.is_legal, assigned=())
    def is_legal(self, *args, **kwargs):
        return self.tiles.is_legal(*args, **kwargs)

    def is_passable(self, coord):
        if coord in self.creatures:
            return False
        else:
            return self.tiles[coord].is_passable

    def is_pathable(self, coord):
        return self.tiles[coord].is_passable

    def is_see_through(self, coord):
        return self.tiles[coord].is_see_through

    def check_los(self, coord_a, coord_b):
        return not (any(not self.is_see_through(coord) for coord in bresenham(coord_a, coord_b)) and
                    any(not self.is_see_through(coord) for coord in bresenham(coord_b, coord_a)))

    def distance(self, coord_a, coord_b):
        return round(path.distance(coord_a, coord_b, Action.Move.base_cost, dir.DiagonalMoveMult))

    def movement_multiplier(self, coord, direction):
        origin_multiplier = self.tiles[coord].movement_multiplier
        target_coord = add_vector(coord, direction)
        target_multiplier = self.tiles[target_coord].movement_multiplier

        tile_multiplier = (origin_multiplier + target_multiplier) / 2
        return tile_multiplier * dir.move_mult(direction)

    # nudge_coord nudges towards a line between end_coord and nudge_coord
    def _a_star_heuristic(self, start_coord, end_coord, nudge_coord):
        cost = self.distance(start_coord, end_coord)
        if Debug.cross:
            cost += cross_product(start_coord, end_coord, nudge_coord) / Debug.cross_mod
        return cost

    def path(self, start_coord, goal_coord):
        return path.path(start_coord, goal_coord, self.get_neighbor_location_coords_and_costs, self._a_star_heuristic)

    def look_information(self, coord):
        # if coord in creature.visited_location_coords:
        information = f"{coord[0]}x{coord[1]} "
        if coord in self.creatures:
            c: Creature = self.creatures[coord]
            damage = c.damage_dice
            information += f"{c.name} hp:{c.hp}/{c.max_hp} sight:{c.sight} armor:{c.armor} dr:{c.defense} " \
                           f"ar:{c.accuracy} attack:{damage.dices}D{damage.faces}+{damage.addition}"
        else:
            information += self.tiles[coord].name
        return information
        # else:
        #     return "You don't know anything about this place."

    def spawn_creature(self, creature):
        coord = None
        if creature.coord is not None:
            assert self.is_passable(creature.coord), \
                f"Attempting to spawn {creature.name} to already occupied square: {creature.coord}"
            coord = creature.coord

        self.add_creature(creature, coord)
        self.turn_scheduler.add(creature, creature.action_cost(Action.Spawn))

    def add_creature_to_location(self, creature, level_location):
        coord = self.get_location_coord(level_location)
        self.add_creature(creature, coord)
        self.turn_scheduler.add(creature, 0)

    def add_creature(self, creature, coord=None):
        if coord is None:
            coord = self.free_coord()
        if coord in self.creatures:
            blocking_creature = self.creatures[coord]
            self.move_creature(blocking_creature, self.free_coord())
        self.creatures[coord] = creature
        creature.coord = coord
        creature.level = self
        self.visible_change.trigger(coord)

    def remove_creature(self, creature):
        coord = creature.coord
        del self.creatures[coord]
        creature.coord = None
        creature.level = None
        self.turn_scheduler.remove(creature)
        self.visible_change.trigger(coord)

    def move_creature(self, creature, new_coord):
        old_coord = creature.coord
        del self.creatures[old_coord]
        self.creatures[new_coord] = creature
        creature.coord = new_coord

        self.visible_change.trigger(old_coord)
        self.visible_change.trigger(new_coord)

    def move_creature_to_dir(self, creature, direction):
        target_coord = add_vector(creature.coord, direction)
        self.move_creature(creature, target_coord)

    def swap_creature(self, creature_a, creature_b):
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

    def add_items(self, coord, items):
        if coord in self.items:
            current_items = self.items[coord]
        else:
            current_items = ()
        self.items[coord] = tuple(itertools.chain(current_items, items))
        self.visible_change.trigger(coord)
