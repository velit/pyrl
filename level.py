from __future__ import absolute_import, division, print_function, unicode_literals

import random

from enum import Enum

import path
from config.debug import Debug
from creature.actions import Action
from creature.creature import Creature
from enums.directions import Dir
from generic_algorithms import bresenham, cross_product, get_vector, add_vector
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
        self.location_coords = level_template.location_coords
        self.visible_change = Event()
        self.turn_scheduler = TurnScheduler()
        self.creatures = {}
        self.generation_type = level_template.generation_type

        for creature in level_template.custom_creatures:
            self.spawn_creature(creature)

        if level_template.creature_spawning:
            self.creature_spawn_list = level_template.get_creature_spawn_list()

            for _ in range(level_template.creature_spawn_count):
                creature = Creature(random.choice(self.creature_spawn_list))
                self.spawn_creature(creature)

    def get_free_coord(self):
        # TODO: improve this at some point
        while True:
            coord = random.randrange(self.rows), random.randrange(self.cols)
            if self.is_passable(coord):
                return coord

    def get_coord_iter(self):
        return ((y, x) for y in range(self.rows) for x in range(self.cols))

    def get_exit_info(self, coord):
        return self.exit_infos[coord]

    def get_creature(self, coord):
        return self.creatures[coord]

    def get_visible_char(self, coord):
        if self.has_creature(coord):
            return self.get_creature(coord).char
        else:
            return self.tiles[coord].visible_char

    def get_memory_char(self, coord):
        return self.tiles[coord].memory_char

    def get_vision_information(self, coords, visible_coords, always_show_creatures=False):
        for coord in coords:
            if coord in visible_coords:
                yield coord, self.get_visible_char(coord)
            else:
                if always_show_creatures and self.has_creature(coord):
                    yield coord, self.get_creature(coord).char
                else:
                    yield coord, self.get_memory_char(coord)

    def get_location(self, coord):
        return self.location_coords.getkey(coord)

    def get_location_coord(self, level_location):
        if level_location == LevelLocation.Random_Location:
            return self.get_free_coord()
        else:
            return self.location_coords[level_location]

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

    def has_creature(self, coord):
        return coord in self.creatures

    def has_location(self, coord):
        return coord in self.location_coords.values()

    def has_location_coord(self, location):
        return location in self.location_coords

    def is_legal(self, *args, **keys):
        return self.tiles.is_legal(*args, **keys)

    def is_passable(self, coord):
        if self.has_creature(coord):
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
        if self.has_creature(coord):
            c = self.get_creature(coord)
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
        self.turn_scheduler.add(creature, creature.action_cost(Action.Move))

    def add_creature_to_location(self, creature, level_location):
        coord = self.get_location_coord(level_location)
        self.add_creature(creature, coord)

    def add_creature(self, creature, coord=None):
        if coord is None:
            coord = self.get_free_coord()

        elif self.has_creature(coord):
            blocking_creature = self.creatures[coord]
            self.move_creature(blocking_creature, self.get_free_coord())
        self.creatures[coord] = creature
        creature.coord = coord
        creature.level = self
        self.visible_change.trigger(coord)

    def remove_creature(self, creature, turnscheduler_remove=True):
        coord = creature.coord
        del self.creatures[coord]
        creature.coord = None
        creature.level = None

        if turnscheduler_remove:
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

    def creature_can_reach(self, creature, target_coord):
        return (creature.coord == target_coord or
            get_vector(creature.coord, target_coord) in Dir.All)

    def creature_can_move(self, creature, direction):
        if direction not in Dir.AllPlusStay:
            raise ValueError("Illegal movement direction: {}".format(direction))
        elif direction == Dir.Stay:
            return True
        else:
            coord = add_vector(creature.coord, direction)
            return self.is_legal(coord) and self.is_passable(coord)

    def creature_target_theoretically_in_sight(self, creature, target_coord):
        cy, cx = creature.coord
        ty, tx = target_coord
        return (cy - ty) ** 2 + (cx - tx) ** 2 <= creature.sight ** 2

    def creature_has_sight(self, creature, target_coord):
        return (self.creature_target_theoretically_in_sight(creature, target_coord) and
                self.check_los(creature.coord, target_coord))
