from __future__ import absolute_import, division, print_function, unicode_literals

import random

import path
import itertools
from enum import Enum
from config.debug import Debug
from creature.actions import Action
from creature.creature import Creature
from enums.directions import Dir
from generic_algorithms import bresenham, cross_product, add_vector
from generic_structures import Event
from turn_scheduler import TurnScheduler


class LevelLocation(Enum):
    Passage_Up      = 1
    Passage_Down    = 2
    Random_Location = 3


class Level(object):

    def __init__(self, level_key, level_template):
        self.key = level_key
        self.tiles = level_template.tiles
        self.rows, self.cols = self.tiles.dimensions
        self.danger_level = level_template.danger_level
        self.locations = level_template.locations
        self.visible_change = Event()
        self.turn_scheduler = TurnScheduler()
        self.creatures = {}
        self.items = {}
        self.generation_type = level_template.generation_type

        for creature in level_template.custom_creatures:
            self.spawn_creature(creature)

        if level_template.creature_spawning:
            self.creature_spawn_list = level_template.get_creature_spawn_list()

            for _ in range(level_template.creature_spawn_count):
                creature = Creature(random.choice(self.creature_spawn_list))
                self.spawn_creature(creature)
        else:
            self.creature_spawn_list = []

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
            yield neighbor_coord, round(multiplier * Action.Move.cost)

    def get_passable_neighbors(self, coord):
        for direction in Dir.All:
            neighbor_coord = add_vector(coord, direction)
            if self.is_legal(neighbor_coord) and self.tiles[neighbor_coord].is_passable:
                yield direction

    def is_legal(self, *args, **keys):
        return self.tiles.is_legal(*args, **keys)

    def is_passable(self, coord):
        if coord in self.creatures:
            return False
        else:
            return self.tiles[coord].is_passable

    def is_pathable(self, coord):
        return self.tiles[coord].is_passable

    def is_see_through(self, coord):
        return self.tiles[coord].is_see_through

    def check_los(self, coordA, coordB):
        return not (any(not self.is_see_through(coord) for coord in bresenham(coordA, coordB)) and
                    any(not self.is_see_through(coord) for coord in bresenham(coordB, coordA)))

    def distance_heuristic(self, coordA, coordB):
        return round(path.heuristic(coordA, coordB, Action.Move.cost, Dir.DiagonalMoveMult))

    def movement_multiplier(self, coord, direction):
        origin_multiplier = self.tiles[coord].movement_multiplier
        target_coord = add_vector(coord, direction)
        target_multiplier = self.tiles[target_coord].movement_multiplier

        tile_multiplier = (origin_multiplier + target_multiplier) / 2
        return tile_multiplier * Dir.move_mult(direction)

    # nudge_coord nudges towards a line between end_coord and nudge_coord
    def _a_star_heuristic(self, start_coord, end_coord, nudge_coord):
        cost = self.distance_heuristic(start_coord, end_coord)
        if Debug.cross:
            cost += cross_product(start_coord, end_coord, nudge_coord) / Debug.cross_mod
        return cost

    def path(self, start_coord, goal_coord):
        return path.path(start_coord, goal_coord, self.get_neighbor_location_coords_and_costs, self._a_star_heuristic)

    def look_information(self, coord):
        #if coord in creature.visited_location_coords:
        information = "{}x{} ".format(*coord)
        if coord in self.creatures:
            c = self.creatures[coord]
            msg = "{} hp:{}/{} sight:{} armor:{} dr:{} ar:{} attack:{}D{}+{}"
            information += msg.format(c.name, c.hp, c.max_hp, c.sight, c.armor,
                                      c.defense_rating, c.attack_rating, *c.get_damage_info())
            if hasattr(c, "target_coord"):
                information += " target:{}".format(c.target_coord)
            if hasattr(c, "chase_vector"):
                information += " direction:{}".format(c.chase_vector)
        else:
            information += self.tiles[coord].name
        return information
        #else:
        #   return "You don't know anything about this place."

    def spawn_creature(self, creature):
        coord = None
        if creature.coord is not None:
            if not self.is_passable(creature.coord):
                fmt = "Attempting to spawn creature {} to already occupied square: {}"
                raise AssertionError(fmt.format(creature.name, creature.coord))
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

        elif coord in self.creatures:
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

    def swap_creature(self, creatureA, creatureB):
        creatureA.coord, creatureB.coord = creatureB.coord, creatureA.coord
        self.creatures[creatureA.coord] = creatureA
        self.creatures[creatureB.coord] = creatureB
        self.visible_change.trigger(creatureA.coord)
        self.visible_change.trigger(creatureB.coord)

    def enumerate_items(self, coord):
        if coord in self.items:
            return enumerate(self.items[coord])
        else:
            return enumerate(())

    def take_items(self, coord, item_indexes):
        if not item_indexes:
            return ()

        assert coord in self.items, "Trying to take items from a coord {} that doesn't have any.".format(coord)

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

    def deposit_items(self, coord, items):
        if coord in self.items:
            current_items = self.items[coord]
        else:
            current_items = ()
        self.items[coord] = tuple(itertools.chain(current_items, items))
        self.visible_change.trigger(coord)
